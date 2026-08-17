from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Initiative, MediaItem, Program, Project


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "our_story",
            "vision_mission",
            "team",
            "governance",
            "privacy_policy",
            "program_list",
            "project_list",
            "media_list",
            "partners",
            "careers",
            "volunteer",
            "csr",
            "donate",
            "events_list",
        ]

    def location(self, item):
        return reverse(item)


class ProgramSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Program.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class MediaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return MediaItem.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class InitiativeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Initiative.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "programs": ProgramSitemap,
    "projects": ProjectSitemap,
    "media": MediaSitemap,
    "initiatives": InitiativeSitemap,
}
