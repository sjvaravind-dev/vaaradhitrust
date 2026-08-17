from django.core.cache import cache

from .models import PopupBanner, Program, ScrollingNews, SiteSettings
from django.utils import timezone


def site_globals(request):
    settings = cache.get("site_settings")
    if settings is None:
        settings = SiteSettings.load()
        cache.set("site_settings", settings, 300)

    news = cache.get("scrolling_news")
    if news is None:
        news = list(ScrollingNews.objects.filter(is_active=True)[:12])
        cache.set("scrolling_news", news, 120)

    popup = cache.get("active_popup")
    if popup is None:
        now = timezone.now()
        popup = None
        for item in PopupBanner.objects.filter(is_active=True)[:5]:
            if item.starts_at and item.starts_at > now:
                continue
            if item.ends_at and item.ends_at < now:
                continue
            popup = item
            break
        cache.set("active_popup", popup, 120)

    programs = cache.get("nav_programs")
    if programs is None:
        programs = list(Program.objects.filter(is_active=True)[:12])
        cache.set("nav_programs", programs, 300)

    return {
        "site": settings,
        "scrolling_news": news,
        "popup_banner": popup,
        "nav_programs": programs,
    }
