from django.core.cache import cache
from django.utils import timezone

from .models import PageHit


class SiteTrafficMiddleware:
    """
    Lightweight path hit counter using cache buffering to stay smooth
    under high request volume (avoids a DB write on every request).
    """

    SKIP_PREFIXES = (
        "/static/",
        "/media/",
        "/admin/",
        "/api/",
        "/favicon",
        "/robots",
        "/sitemap",
    )
    BUFFER_KEY = "traffic_buffer"
    FLUSH_EVERY = 25

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if any(path.startswith(p) for p in self.SKIP_PREFIXES):
            return response
        if request.method != "GET":
            return response
        if response.status_code >= 400:
            return response

        try:
            buffer = cache.get(self.BUFFER_KEY) or {}
            buffer[path] = buffer.get(path, 0) + 1
            total = sum(buffer.values())
            if total >= self.FLUSH_EVERY:
                self._flush(buffer)
                cache.set(self.BUFFER_KEY, {}, 3600)
            else:
                cache.set(self.BUFFER_KEY, buffer, 3600)
        except Exception:
            pass
        return response

    def _flush(self, buffer):
        for path, count in buffer.items():
            obj, created = PageHit.objects.get_or_create(path=path, defaults={"hits": count})
            if not created:
                PageHit.objects.filter(pk=obj.pk).update(
                    hits=obj.hits + count, last_hit=timezone.now()
                )
