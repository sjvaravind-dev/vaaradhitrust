from rest_framework import serializers

from core.models import (
    Career,
    DonationCampaign,
    Event,
    HomeSlider,
    ImpactStat,
    Initiative,
    MediaItem,
    Partner,
    PopupBanner,
    Program,
    Project,
    ScrollingNews,
    SiteSettings,
    TeamMember,
    Testimonial,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        exclude = ("id",)


class ScrollingNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrollingNews
        fields = ("id", "text", "link", "order")


class PopupBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopupBanner
        fields = ("id", "title", "image", "link", "button_text")


class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = (
            "id",
            "title",
            "subtitle",
            "theme",
            "background_image",
            "cta_text",
            "cta_link",
            "overlay_color",
            "order",
        )


class ImpactStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStat
        fields = ("id", "label", "value", "icon", "order")


class InitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "image",
            "donate_link",
            "order",
        )


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "icon_key",
            "image",
            "order",
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "slug",
            "category",
            "status",
            "summary",
            "description",
            "image",
            "partner_name",
            "order",
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "slug",
            "event_type",
            "summary",
            "event_date",
            "location",
            "image",
            "external_url",
        )


class MediaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = (
            "id",
            "title",
            "slug",
            "excerpt",
            "body",
            "image",
            "external_url",
            "published_at",
        )


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ("id", "name", "partner_type", "logo", "brief", "website", "order")


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ("id", "name", "role_label", "role_type", "quote", "photo", "order")


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = (
            "id",
            "name",
            "designation",
            "category",
            "bio",
            "photo",
            "linkedin_url",
            "order",
        )


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            "id",
            "title",
            "slug",
            "location",
            "employment_type",
            "summary",
            "description",
            "apply_email",
            "apply_url",
            "posted_at",
        )


class DonationCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCampaign
        fields = (
            "id",
            "title",
            "slug",
            "summary",
            "description",
            "image",
            "goal_amount",
            "raised_amount",
            "donate_url",
        )


class DonationCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=160)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    pan = serializers.CharField(max_length=10, required=False, allow_blank=True)
    cause = serializers.CharField(max_length=80)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    donation_type = serializers.ChoiceField(choices=["one-time", "monthly"])
    updates = serializers.BooleanField(required=False, default=False)
    payment_method = serializers.ChoiceField(
        choices=["upi", "google_pay", "phonepe", "card", "netbanking"],
        required=False,
        default="upi",
    )

    def validate_pan(self, value):
        value = (value or "").strip().upper()
        if value and len(value) != 10:
            raise serializers.ValidationError("PAN must be 10 characters.")
        return value

    def validate_amount(self, value):
        from django.conf import settings

        minimum = settings.DONATION_MIN_AMOUNT
        if value < minimum:
            raise serializers.ValidationError(f"Minimum online donation is ₹{minimum}.")
        return value


class DonationVerifySerializer(serializers.Serializer):
    donation_id = serializers.IntegerField()
    razorpay_order_id = serializers.CharField(required=False, allow_blank=True)
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
    razorpay_subscription_id = serializers.CharField(required=False, allow_blank=True)
