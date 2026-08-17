import json

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Donation, DonationCampaign, SiteSettings
from core.razorpay_client import (
    get_client,
    is_configured,
    verify_payment_signature,
    verify_subscription_signature,
    verify_webhook_signature,
)

from .serializers import DonationCreateSerializer, DonationVerifySerializer

WHEREVER_NEEDED = "wherever-needed"
WHEREVER_TITLE = "Wherever It's Needed Most"


def _cause_title(slug):
    if slug == WHEREVER_NEEDED:
        return WHEREVER_TITLE
    campaign = DonationCampaign.objects.filter(slug=slug, is_active=True).first()
    return campaign.title if campaign else None


class DonationConfigView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response(
            {
                "configured": is_configured(),
                "key_id": settings.RAZORPAY_KEY_ID,
                "min_amount": settings.DONATION_MIN_AMOUNT,
                "currency": "INR",
            }
        )


class DonationCreateOrderView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = DonationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cause_slug = data["cause"]
        cause_title = _cause_title(cause_slug)
        if not cause_title:
            return Response({"detail": "Please choose a valid cause."}, status=400)

        campaign = DonationCampaign.objects.filter(slug=cause_slug, is_active=True).first()
        payment_method = data.get("payment_method") or "upi"
        donation = Donation.objects.create(
            name=data["name"].strip(),
            email=data["email"].strip(),
            phone=(data.get("phone") or "").strip(),
            pan=(data.get("pan") or "").strip().upper(),
            cause_slug=cause_slug,
            cause_title=cause_title,
            amount=data["amount"],
            donation_type=data["donation_type"],
            send_updates=bool(data.get("updates")),
            campaign=campaign,
            status=Donation.STATUS_PENDING,
            notes=f"payment_method={payment_method}",
        )

        if not is_configured():
            return Response(
                {
                    "configured": False,
                    "donation_id": donation.id,
                    "detail": (
                        "Razorpay keys are not added yet. Set RAZORPAY_KEY_ID and "
                        "RAZORPAY_KEY_SECRET in .env, then restart the server."
                    ),
                },
                status=503,
            )

        client = get_client()
        site = SiteSettings.load()
        amount_paise = donation.amount_paise
        notes = {
            "donation_id": str(donation.id),
            "cause": cause_title,
            "donor": donation.name,
            "pan": donation.pan,
            "payment_method": payment_method,
        }

        try:
            if donation.donation_type == Donation.TYPE_MONTHLY:
                plan = client.plan.create(
                    {
                        "period": "monthly",
                        "interval": 1,
                        "item": {
                            "name": f"Monthly · {cause_title}",
                            "amount": amount_paise,
                            "currency": "INR",
                            "description": f"Monthly donation to {site.org_name}",
                        },
                    }
                )
                subscription = client.subscription.create(
                    {
                        "plan_id": plan["id"],
                        "customer_notify": 1,
                        "total_count": 120,
                        "notes": notes,
                    }
                )
                donation.razorpay_subscription_id = subscription["id"]
                donation.save(update_fields=["razorpay_subscription_id", "updated_at"])
                checkout = {"subscription_id": subscription["id"], "order_id": ""}
            else:
                order = client.order.create(
                    {
                        "amount": amount_paise,
                        "currency": "INR",
                        "receipt": f"don_{donation.id}",
                        "payment_capture": 1,
                        "notes": notes,
                    }
                )
                donation.razorpay_order_id = order["id"]
                donation.save(update_fields=["razorpay_order_id", "updated_at"])
                checkout = {"order_id": order["id"], "subscription_id": ""}
        except Exception as exc:
            donation.status = Donation.STATUS_FAILED
            donation.notes = str(exc)
            donation.save(update_fields=["status", "notes", "updated_at"])
            return Response(
                {"detail": "Could not start Razorpay checkout. Please try again."},
                status=502,
            )

        return Response(
            {
                "configured": True,
                "donation_id": donation.id,
                "key_id": settings.RAZORPAY_KEY_ID,
                "amount": amount_paise,
                "currency": "INR",
                "name": site.org_name,
                "description": cause_title,
                "prefill": {
                    "name": donation.name,
                    "email": donation.email,
                    "contact": donation.phone,
                },
                "notes": notes,
                "theme": {"color": "#c45c26"},
                **checkout,
            }
        )


class DonationVerifyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = DonationVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        donation = Donation.objects.filter(pk=data["donation_id"]).first()
        if not donation:
            return Response({"detail": "Donation not found."}, status=404)

        payment_id = data["razorpay_payment_id"]
        signature = data["razorpay_signature"]
        order_id = data.get("razorpay_order_id") or donation.razorpay_order_id
        subscription_id = (
            data.get("razorpay_subscription_id") or donation.razorpay_subscription_id
        )

        if donation.donation_type == Donation.TYPE_MONTHLY:
            valid = verify_subscription_signature(payment_id, subscription_id, signature)
        else:
            valid = verify_payment_signature(order_id, payment_id, signature)

        if not valid:
            donation.status = Donation.STATUS_FAILED
            donation.razorpay_payment_id = payment_id
            donation.razorpay_signature = signature
            donation.save(
                update_fields=[
                    "status",
                    "razorpay_payment_id",
                    "razorpay_signature",
                    "updated_at",
                ]
            )
            return Response(
                {"detail": "Payment signature could not be verified."}, status=400
            )

        donation.status = Donation.STATUS_PAID
        donation.razorpay_payment_id = payment_id
        donation.razorpay_signature = signature
        if order_id:
            donation.razorpay_order_id = order_id
        if subscription_id:
            donation.razorpay_subscription_id = subscription_id
        donation.save()

        if donation.campaign_id:
            campaign = donation.campaign
            campaign.raised_amount = (campaign.raised_amount or 0) + donation.amount
            campaign.save(update_fields=["raised_amount", "updated_at"])

        return Response(
            {
                "ok": True,
                "donation_id": donation.id,
                "redirect": f"/donate/thank-you/?id={donation.id}",
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class DonationWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        signature = request.META.get("HTTP_X_RAZORPAY_SIGNATURE", "")
        body = request.body
        if settings.RAZORPAY_WEBHOOK_SECRET and not verify_webhook_signature(
            body, signature
        ):
            return Response({"detail": "Invalid webhook signature."}, status=400)

        try:
            payload = json.loads(body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON."}, status=400)

        event = payload.get("event", "")
        entity = (payload.get("payload") or {}).get("payment", {}).get("entity") or {}
        payment_id = entity.get("id", "")
        order_id = entity.get("order_id", "")
        notes = entity.get("notes") or {}
        donation = None
        if notes.get("donation_id"):
            donation = Donation.objects.filter(pk=notes["donation_id"]).first()
        if not donation and order_id:
            donation = Donation.objects.filter(razorpay_order_id=order_id).first()
        if not donation and payment_id:
            donation = Donation.objects.filter(razorpay_payment_id=payment_id).first()

        if donation:
            if event in ("payment.captured", "order.paid"):
                donation.status = Donation.STATUS_PAID
            elif event in ("payment.failed",):
                donation.status = Donation.STATUS_FAILED
            if payment_id:
                donation.razorpay_payment_id = payment_id
            donation.save()

        return Response({"ok": True})
