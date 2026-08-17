from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .donations import (
    DonationConfigView,
    DonationCreateOrderView,
    DonationVerifyView,
    DonationWebhookView,
)
from .views import (
    CareerViewSet,
    DonationCampaignViewSet,
    EventViewSet,
    HomeBundleView,
    HomeSliderViewSet,
    ImpactStatViewSet,
    InitiativeViewSet,
    MediaItemViewSet,
    PartnerViewSet,
    PopupBannerViewSet,
    ProgramViewSet,
    ProjectViewSet,
    ScrollingNewsViewSet,
    SiteSettingsView,
    TeamMemberViewSet,
    TestimonialViewSet,
)

router = DefaultRouter()
router.register("news-ticker", ScrollingNewsViewSet, basename="news-ticker")
router.register("popups", PopupBannerViewSet, basename="popups")
router.register("sliders", HomeSliderViewSet, basename="sliders")
router.register("impact", ImpactStatViewSet, basename="impact")
router.register("initiatives", InitiativeViewSet, basename="initiatives")
router.register("programs", ProgramViewSet, basename="programs")
router.register("projects", ProjectViewSet, basename="projects")
router.register("events", EventViewSet, basename="events")
router.register("media", MediaItemViewSet, basename="media")
router.register("partners", PartnerViewSet, basename="partners")
router.register("testimonials", TestimonialViewSet, basename="testimonials")
router.register("team", TeamMemberViewSet, basename="team")
router.register("careers", CareerViewSet, basename="careers")
router.register("campaigns", DonationCampaignViewSet, basename="campaigns")

urlpatterns = [
    path("settings/", SiteSettingsView.as_view(), name="api-settings"),
    path("home/", HomeBundleView.as_view(), name="api-home"),
    path("donations/config/", DonationConfigView.as_view(), name="api-donation-config"),
    path("donations/orders/", DonationCreateOrderView.as_view(), name="api-donation-orders"),
    path("donations/verify/", DonationVerifyView.as_view(), name="api-donation-verify"),
    path("donations/webhook/", DonationWebhookView.as_view(), name="api-donation-webhook"),
    path("", include(router.urls)),
]
