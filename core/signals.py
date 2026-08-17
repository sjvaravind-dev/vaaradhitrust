from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

CACHE_KEYS = (
    "site_settings",
    "scrolling_news",
    "active_popup",
    "nav_programs",
)


def clear_site_caches(**kwargs):
    for key in CACHE_KEYS:
        cache.delete(key)


@receiver(post_save)
@receiver(post_delete)
def invalidate_on_change(sender, **kwargs):
    app_label = getattr(getattr(sender, "_meta", None), "app_label", None)
    if app_label == "core":
        clear_site_caches()
