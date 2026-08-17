from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from .models import (
    Career,
    Donation,
    DonationCampaign,
    Event,
    GovernanceDocument,
    HomeSlider,
    ImpactStat,
    Initiative,
    MediaItem,
    Partner,
    Program,
    Project,
    SiteSettings,
    TeamMember,
    Testimonial,
)


def _seo(context, title=None, description=None, keywords=None, canonical=None, image=None):
    site = context.get("site") or SiteSettings.load()
    context["seo"] = {
        "title": title or site.meta_title,
        "description": description or site.meta_description,
        "keywords": keywords or site.meta_keywords,
        "canonical": canonical,
        "image": image,
        "og_type": "website",
    }
    return context


@cache_page(60)
@require_GET
def home(request):
    ctx = {
        "sliders": HomeSlider.objects.filter(is_active=True)[:8],
        "impact_stats": ImpactStat.objects.filter(is_active=True)[:4],
        "initiatives": Initiative.objects.filter(is_active=True, is_featured=True)[:8],
        "programs": Program.objects.filter(is_active=True)[:8],
        "active_projects": Project.objects.filter(
            is_active=True, status=Project.STATUS_ACTIVE
        )[:6],
        "partners": Partner.objects.filter(is_active=True)[:16],
        "testimonials": Testimonial.objects.filter(is_active=True)[:8],
        "events": Event.objects.filter(is_active=True)[:4],
        "media_items": MediaItem.objects.filter(is_active=True)[:4],
        "campaigns": DonationCampaign.objects.filter(is_active=True, is_featured=True)[:3],
    }
    return render(request, "pages/home.html", _seo(ctx))


@cache_page(120)
@require_GET
def our_story(request):
    site = SiteSettings.load()
    ctx = {"page_title": "Our Story"}
    return render(
        request,
        "pages/our_story.html",
        _seo(
            ctx,
            title=f"Our Story | {site.org_name}",
            description="How Vaaradhi Trust was founded to bridge surplus with unmet need across communities in India.",
        ),
    )


@cache_page(120)
@require_GET
def vision_mission(request):
    site = SiteSettings.load()
    ctx = {"page_title": "Vision & Mission"}
    return render(
        request,
        "pages/vision_mission.html",
        _seo(ctx, title=f"Vision & Mission | {site.org_name}"),
    )


@cache_page(60)
@require_GET
def team(request):
    site = SiteSettings.load()
    members = TeamMember.objects.filter(is_active=True)
    ctx = {
        "page_title": "Our Team",
        "board": members.filter(category=TeamMember.CATEGORY_BOARD),
        "team": members.filter(category=TeamMember.CATEGORY_TEAM),
        "advisors": members.filter(category=TeamMember.CATEGORY_ADVISOR),
    }
    return render(
        request,
        "pages/team.html",
        _seo(ctx, title=f"Our Team | {site.org_name}"),
    )


@cache_page(120)
@require_GET
def governance(request):
    site = SiteSettings.load()
    ctx = {
        "page_title": "Governance",
        "documents": GovernanceDocument.objects.filter(is_active=True),
    }
    return render(
        request,
        "pages/governance.html",
        _seo(ctx, title=f"Governance | {site.org_name}"),
    )


@cache_page(300)
@require_GET
def privacy_policy(request):
    site = SiteSettings.load()
    ctx = {"page_title": "Privacy Policy"}
    return render(
        request,
        "pages/privacy.html",
        _seo(ctx, title=f"Privacy Policy | {site.org_name}"),
    )


@cache_page(60)
@require_GET
def media_list(request):
    site = SiteSettings.load()
    items = MediaItem.objects.filter(is_active=True)
    ctx = {"page_title": "Media & News", "items": items}
    return render(
        request,
        "pages/media_list.html",
        _seo(
            ctx,
            title=f"Media & News | {site.org_name}",
            description="Latest updates, meetings and field visits from Vaaradhi Trust.",
        ),
    )


@cache_page(60)
@require_GET
def media_detail(request, slug):
    item = get_object_or_404(MediaItem, slug=slug, is_active=True)
    ctx = {"item": item, "page_title": item.title}
    return render(
        request,
        "pages/media_detail.html",
        _seo(
            ctx,
            title=item.meta_title or f"{item.title} | Vaaradhi Trust",
            description=item.meta_description or item.excerpt[:160],
        ),
    )


@cache_page(60)
@require_GET
def program_list(request):
    site = SiteSettings.load()
    ctx = {
        "page_title": "Our Programs",
        "programs": Program.objects.filter(is_active=True),
    }
    return render(
        request,
        "pages/program_list.html",
        _seo(ctx, title=f"Programs | {site.org_name}"),
    )


@cache_page(60)
@require_GET
def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, is_active=True)
    ctx = {
        "program": program,
        "page_title": program.title,
        "projects": program.projects.filter(is_active=True)[:8],
    }
    return render(
        request,
        "pages/program_detail.html",
        _seo(
            ctx,
            title=program.meta_title or f"{program.title} | Vaaradhi Trust",
            description=program.meta_description or program.short_description[:160],
        ),
    )


@cache_page(60)
@require_GET
def project_list(request):
    status = request.GET.get("status", "active")
    site = SiteSettings.load()
    qs = Project.objects.filter(is_active=True)
    if status == "ongoing":
        qs = qs.filter(status=Project.STATUS_ONGOING)
        title = "Ongoing Projects"
    elif status == "upcoming":
        qs = qs.filter(status=Project.STATUS_UPCOMING)
        title = "Upcoming Projects"
    else:
        qs = qs.filter(Q(status=Project.STATUS_ACTIVE) | Q(status=Project.STATUS_ONGOING))
        if status == "active":
            qs = Project.objects.filter(is_active=True, status=Project.STATUS_ACTIVE)
            title = "Active Projects"
        else:
            title = "Our Work"
    ctx = {"page_title": title, "projects": qs, "status": status}
    return render(
        request,
        "pages/project_list.html",
        _seo(ctx, title=f"{title} | {site.org_name}"),
    )


@cache_page(60)
@require_GET
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    ctx = {"project": project, "page_title": project.title}
    return render(
        request,
        "pages/project_detail.html",
        _seo(ctx, title=f"{project.title} | Vaaradhi Trust", description=project.summary[:160]),
    )


@cache_page(60)
@require_GET
def initiative_detail(request, slug):
    item = get_object_or_404(Initiative, slug=slug, is_active=True)
    ctx = {"initiative": item, "page_title": item.title}
    return render(
        request,
        "pages/initiative_detail.html",
        _seo(ctx, title=f"{item.title} | Vaaradhi Trust"),
    )


@require_GET
def events_redirect(request):
    """Events nav/home CTA redirects to Vaaradhi Trust LinkedIn."""
    site = SiteSettings.load()
    url = site.events_linkedin_url or site.linkedin_url
    if url:
        return HttpResponseRedirect(url)
    return redirect("home")


@cache_page(60)
@require_GET
def events_list(request):
    """Internal events archive (still available); nav links use LinkedIn redirect."""
    site = SiteSettings.load()
    ctx = {
        "page_title": "Events",
        "events": Event.objects.filter(is_active=True),
        "linkedin_url": site.events_linkedin_url or site.linkedin_url,
    }
    return render(
        request,
        "pages/events_list.html",
        _seo(ctx, title=f"Events | {site.org_name}"),
    )


@cache_page(60)
@require_GET
def partners(request):
    site = SiteSettings.load()
    ctx = {
        "page_title": "Our Partners",
        "partners": Partner.objects.filter(is_active=True),
    }
    return render(
        request,
        "pages/partners.html",
        _seo(ctx, title=f"Our Partners | {site.org_name}"),
    )


@cache_page(60)
@require_GET
def careers(request):
    site = SiteSettings.load()
    ctx = {
        "page_title": "Careers",
        "vacancies": Career.objects.filter(is_open=True),
    }
    return render(
        request,
        "pages/careers.html",
        _seo(
            ctx,
            title=f"Careers | {site.org_name}",
            description="Build a career that creates impact at Vaaradhi Trust.",
        ),
    )


@cache_page(120)
@require_GET
def volunteer(request):
    site = SiteSettings.load()
    ctx = {"page_title": "Volunteer With Us"}
    return render(
        request,
        "pages/volunteer.html",
        _seo(ctx, title=f"Volunteer With Us | {site.org_name}"),
    )


@cache_page(120)
@require_GET
def csr(request):
    site = SiteSettings.load()
    ctx = {"page_title": "CSR Partnership Facilitation"}
    return render(
        request,
        "pages/csr.html",
        _seo(ctx, title=f"CSR Partnership | {site.org_name}"),
    )


@require_GET
def donate(request):
    from django.conf import settings as dj_settings

    site = SiteSettings.load()
    ctx = {
        "page_title": "Donate Now",
        "campaigns": DonationCampaign.objects.filter(is_active=True).order_by("order"),
        "selected_cause": request.GET.get("cause", ""),
        "razorpay_key_id": dj_settings.RAZORPAY_KEY_ID,
        "razorpay_configured": bool(
            dj_settings.RAZORPAY_KEY_ID and dj_settings.RAZORPAY_KEY_SECRET
        ),
        "donation_min_amount": dj_settings.DONATION_MIN_AMOUNT,
    }
    return render(
        request,
        "pages/donate.html",
        _seo(
            ctx,
            title=f"Donate Now | {site.org_name}",
            description=(
                "Choose a cause and create lasting impact with Vaaradhi Trust. "
                "80G eligible donations for urban forestry, skills, generics, education and more."
            ),
        ),
    )


@require_GET
def donate_thank_you(request):
    site = SiteSettings.load()
    donation = None
    donation_id = request.GET.get("id")
    if donation_id:
        donation = Donation.objects.filter(
            pk=donation_id, status=Donation.STATUS_PAID
        ).first()
    ctx = {"page_title": "Thank you", "donation": donation}
    return render(
        request,
        "pages/donate_thank_you.html",
        _seo(ctx, title=f"Thank you | {site.org_name}"),
    )


@require_GET
def donate_failed(request):
    site = SiteSettings.load()
    ctx = {"page_title": "Payment not completed"}
    return render(
        request,
        "pages/donate_failed.html",
        _seo(ctx, title=f"Payment not completed | {site.org_name}"),
    )
