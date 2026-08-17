from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/our-story/", views.our_story, name="our_story"),
    path("about/vision-mission/", views.vision_mission, name="vision_mission"),
    path("about/team/", views.team, name="team"),
    path("about/governance/", views.governance, name="governance"),
    path("about/privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("programs/", views.program_list, name="program_list"),
    path("programs/<slug:slug>/", views.program_detail, name="program_detail"),
    path("work/", views.project_list, name="project_list"),
    path("work/<slug:slug>/", views.project_detail, name="project_detail"),
    path("initiatives/<slug:slug>/", views.initiative_detail, name="initiative_detail"),
    path("media/", views.media_list, name="media_list"),
    path("media/<slug:slug>/", views.media_detail, name="media_detail"),
    path("events/", views.events_list, name="events_list"),
    path("events/linkedin/", views.events_redirect, name="events_linkedin"),
    path("partners/", views.partners, name="partners"),
    path("join-us/careers/", views.careers, name="careers"),
    path("join-us/volunteer/", views.volunteer, name="volunteer"),
    path("join-us/csr/", views.csr, name="csr"),
    path("donate/", views.donate, name="donate"),
    path("donate/thank-you/", views.donate_thank_you, name="donate_thank_you"),
    path("donate/failed/", views.donate_failed, name="donate_failed"),
]
