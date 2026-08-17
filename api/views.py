from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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

from .serializers import (
    CareerSerializer,
    DonationCampaignSerializer,
    EventSerializer,
    HomeSliderSerializer,
    ImpactStatSerializer,
    InitiativeSerializer,
    MediaItemSerializer,
    PartnerSerializer,
    PopupBannerSerializer,
    ProgramSerializer,
    ProjectSerializer,
    ScrollingNewsSerializer,
    SiteSettingsSerializer,
    TeamMemberSerializer,
    TestimonialSerializer,
)


class CachedReadOnlyModelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only API with short response caching for high traffic."""

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SiteSettingsView(APIView):
    @method_decorator(cache_page(120))
    def get(self, request):
        return Response(SiteSettingsSerializer(SiteSettings.load()).data)


class ScrollingNewsViewSet(CachedReadOnlyModelViewSet):
    queryset = ScrollingNews.objects.filter(is_active=True)
    serializer_class = ScrollingNewsSerializer


class PopupBannerViewSet(CachedReadOnlyModelViewSet):
    queryset = PopupBanner.objects.filter(is_active=True)
    serializer_class = PopupBannerSerializer


class HomeSliderViewSet(CachedReadOnlyModelViewSet):
    queryset = HomeSlider.objects.filter(is_active=True)
    serializer_class = HomeSliderSerializer


class ImpactStatViewSet(CachedReadOnlyModelViewSet):
    queryset = ImpactStat.objects.filter(is_active=True)
    serializer_class = ImpactStatSerializer


class InitiativeViewSet(CachedReadOnlyModelViewSet):
    queryset = Initiative.objects.filter(is_active=True)
    serializer_class = InitiativeSerializer
    lookup_field = "slug"


class ProgramViewSet(CachedReadOnlyModelViewSet):
    queryset = Program.objects.filter(is_active=True)
    serializer_class = ProgramSerializer
    lookup_field = "slug"


class ProjectViewSet(CachedReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "slug"
    filterset_fields = ("status", "category")

    def get_queryset(self):
        return Project.objects.filter(is_active=True)


class EventViewSet(CachedReadOnlyModelViewSet):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    lookup_field = "slug"
    filterset_fields = ("event_type",)


class MediaItemViewSet(CachedReadOnlyModelViewSet):
    queryset = MediaItem.objects.filter(is_active=True)
    serializer_class = MediaItemSerializer
    lookup_field = "slug"
    search_fields = ("title", "excerpt")


class PartnerViewSet(CachedReadOnlyModelViewSet):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    filterset_fields = ("partner_type",)


class TestimonialViewSet(CachedReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer
    filterset_fields = ("role_type",)


class TeamMemberViewSet(CachedReadOnlyModelViewSet):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    filterset_fields = ("category",)


class CareerViewSet(CachedReadOnlyModelViewSet):
    queryset = Career.objects.filter(is_open=True)
    serializer_class = CareerSerializer
    lookup_field = "slug"


class DonationCampaignViewSet(CachedReadOnlyModelViewSet):
    queryset = DonationCampaign.objects.filter(is_active=True)
    serializer_class = DonationCampaignSerializer
    lookup_field = "slug"


class HomeBundleView(APIView):
    """Single endpoint for home dynamic blocks — fewer round-trips under load."""

    @method_decorator(cache_page(60))
    def get(self, request):
        return Response(
            {
                "sliders": HomeSliderSerializer(
                    HomeSlider.objects.filter(is_active=True)[:8], many=True, context={"request": request}
                ).data,
                "impact": ImpactStatSerializer(
                    ImpactStat.objects.filter(is_active=True)[:8], many=True
                ).data,
                "initiatives": InitiativeSerializer(
                    Initiative.objects.filter(is_active=True, is_featured=True)[:8],
                    many=True,
                    context={"request": request},
                ).data,
                "partners": PartnerSerializer(
                    Partner.objects.filter(is_active=True)[:16],
                    many=True,
                    context={"request": request},
                ).data,
                "testimonials": TestimonialSerializer(
                    Testimonial.objects.filter(is_active=True)[:8],
                    many=True,
                    context={"request": request},
                ).data,
                "news": ScrollingNewsSerializer(
                    ScrollingNews.objects.filter(is_active=True)[:12], many=True
                ).data,
            }
        )
