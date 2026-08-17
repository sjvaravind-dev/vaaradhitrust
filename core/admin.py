from django.contrib import admin

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
    PageHit,
    Partner,
    PopupBanner,
    Program,
    Project,
    ScrollingNews,
    SiteSettings,
    TeamMember,
    Testimonial,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand", {"fields": ("org_name", "tagline", "logo")}),
        ("Contact", {"fields": ("phone", "email", "address")}),
        (
            "Social & Links",
            {
                "fields": (
                    "facebook_url",
                    "instagram_url",
                    "twitter_url",
                    "youtube_url",
                    "linkedin_url",
                    "events_linkedin_url",
                    "donate_url",
                    "volunteer_url",
                )
            },
        ),
        (
            "Home — Who We Are",
            {
                "fields": (
                    "who_we_are_title",
                    "who_we_are_text",
                    "who_we_are_media",
                    "who_we_are_media_is_video",
                    "vision",
                    "mission",
                )
            },
        ),
        (
            "Our Story",
            {"fields": ("story_quote", "story_quote_author", "story_body")},
        ),
        ("Static pages", {"fields": ("privacy_policy", "volunteer_content", "csr_content", "footer_about")}),
        ("SEO defaults", {"fields": ("meta_title", "meta_description", "meta_keywords")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ScrollingNews)
class ScrollingNewsAdmin(admin.ModelAdmin):
    list_display = ("text", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)


@admin.register(PopupBanner)
class PopupBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "starts_at", "ends_at")
    list_filter = ("is_active",)


@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ("title", "theme", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("theme", "is_active")


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "is_active", "order")
    list_editable = ("value", "is_active", "order")


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "order")
    list_editable = ("is_featured", "is_active", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_editable = ("is_active", "order")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "is_featured", "is_active", "order")
    list_filter = ("status", "is_active", "is_featured")
    list_editable = ("status", "is_featured", "is_active", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "category")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "event_date", "is_featured", "is_active")
    list_filter = ("event_type", "is_active", "is_featured")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_active", "order")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "is_active", "order")
    list_filter = ("partner_type", "is_active")
    list_editable = ("is_active", "order")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role_type", "is_active", "order")
    list_filter = ("role_type", "is_active")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "category", "is_active", "order")
    list_filter = ("category", "is_active")
    list_editable = ("is_active", "order")


@admin.register(GovernanceDocument)
class GovernanceDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "is_active", "order")
    list_filter = ("year", "is_active")


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "is_open", "posted_at")
    list_filter = ("is_open",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(DonationCampaign)
class DonationCampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "order")
    list_editable = ("is_featured", "is_active", "order")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "amount",
        "cause_title",
        "donation_type",
        "status",
        "created_at",
    )
    list_filter = ("status", "donation_type", "cause_slug")
    search_fields = (
        "name",
        "email",
        "phone",
        "pan",
        "razorpay_payment_id",
        "razorpay_order_id",
    )
    readonly_fields = (
        "razorpay_order_id",
        "razorpay_payment_id",
        "razorpay_subscription_id",
        "razorpay_signature",
        "created_at",
        "updated_at",
    )


@admin.register(PageHit)
class PageHitAdmin(admin.ModelAdmin):
    list_display = ("path", "hits", "last_hit")
    search_fields = ("path",)
    readonly_fields = ("path", "hits", "last_hit")
