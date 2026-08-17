from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    Career,
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
    ScrollingNews,
    SiteSettings,
    TeamMember,
    Testimonial,
)


STORY = """Vaaradhi Trust was founded on a simple, timeless belief: that surplus, when guided by purpose, can create lasting social good. It is a philosophy articulated most profoundly by Mahatma Gandhi and one that remains deeply relevant today. There is often enough knowledge to be shared, medicines to be accessed, expertise to be applied, and opportunities to be created. The challenge has rarely been the absence of resources; it has been the gap between what is available and those who need it most. This idea of connecting surplus with unmet need became the foundation of Vaaradhi Trust.

Established in September 2025 in Hyderabad by Mr. Subbarao Kattamuri, Vaaradhi Trust reflects this philosophy in action. Inspired by the belief that success finds its highest purpose when it creates opportunities for others, Mr. Kattamuri chose to dedicate his knowledge, experience, and resources to serving society in a purposeful and enduring way. Through Vaaradhi Trust, that vision has evolved into a platform that bridges critical gaps and creates sustainable pathways for individuals and communities to thrive.

Today, Vaaradhi Trust is a not-for-profit organization committed to designing and implementing high-impact social, environmental, and community-driven initiatives. By fostering meaningful partnerships with government institutions, corporate organizations, academic institutions, and civil society organizations, the Trust brings together diverse expertise and resources to address real-world challenges with sustainable solutions.

With its headquarters in Hyderabad, Vaaradhi Trust is dedicated to empowering underserved communities through focused interventions in various objectives identified. Its objectives span multiple focus areas, including Skill Development, Urban Forestry, Public Health, Education, Legal Awareness & Civic Engagement, Plastic Waste Management, and Strengthening Farmer Producer Organizations (FPOs). Some of the initiatives currently under active intervention are skill development, urban forestry, and public health. Every initiative is guided by a belief that lasting social change is built through collaboration, innovation, and compassion - creating pathways that enable individuals and communities not merely to survive, but to thrive with dignity and hope."""


class Command(BaseCommand):
    help = "Seed Vaaradhi Trust baseline content for local/demo use"

    def handle(self, *args, **options):
        site = SiteSettings.load()
        site.org_name = "Vaaradhi Trust"
        site.tagline = "Bridging Communities With Care"
        site.phone = "+91 7674996876"
        site.email = "contact@vaaradhi.org.in"
        site.linkedin_url = "https://www.linkedin.com/company/vaaradhi-trust/"
        site.events_linkedin_url = "https://www.linkedin.com/company/vaaradhi-trust/"
        site.story_quote = "The world has enough for everyone's need, but not everyone's greed."
        site.story_quote_author = "Mahatma Gandhi"
        site.story_body = STORY
        site.vision = (
            "To build a resilient and equitable society where every individual "
            "and community has the opportunity to thrive with dignity."
        )
        site.mission = (
            "To bridge communities with care by connecting surplus resources, "
            "expertise, and intent to unmet needs through collaborative, "
            "high-impact social and environmental initiatives."
        )
        site.save()

        news = [
            "MoU with National Academy of Construction (NAC) for youth skill development",
            "Exploring student engagement with School of Public Policy and Governance",
            "Urban forestry collaboration with Voon Hands Foundation at Narsapur",
            "Awareness on generic medicines and PMBJP implementation discussions",
        ]
        if not ScrollingNews.objects.exists():
            for i, text in enumerate(news):
                ScrollingNews.objects.create(text=text, order=i, link="/media/")

        sliders = [
            ("Building Capacity", "We equip youth and underserved communities with industry-relevant skills", "skills", "/programs/skill-development/"),
            ("Creating Careers", "Practical training and pathways to dignified employment and entrepreneurship", "careers", "/work/?status=active"),
            ("Empowering Youth = Empowering India", "Skill pathways that unlock opportunity for the next generation", "youth", "/donate/"),
            ("Greening Cities", "Urban forestry and community-led green initiatives", "green", "/programs/urban-forestry/"),
            ("Securing Futures", "We restore ecosystems, enhance biodiversity, and make cities healthier", "futures", "/programs/urban-forestry/"),
            ("Health Equity", "Improving access to affordable healthcare and generic medicines", "health", "/programs/generic-medicines/"),
            ("For Every Community", "Preventive awareness and community-driven health solutions", "community", "/programs/generic-medicines/"),
        ]
        if not HomeSlider.objects.exists():
            for i, (title, sub, theme, link) in enumerate(sliders):
                HomeSlider.objects.create(
                    title=title,
                    subtitle=sub,
                    theme=theme,
                    cta_text="Explore",
                    cta_link=link,
                    order=i,
                )

        stats = [
            ("Telangana", "1", "location", 0),
            ("Key Areas", "7", "areas", 1),
            ("Active Projects", "5", "projects", 2),
            ("Beneficiaries Impacted", "15100+", "people", 3),
        ]
        if not ImpactStat.objects.exists():
            for label, value, icon, order in stats:
                ImpactStat.objects.create(label=label, value=value, icon=icon, order=order)

        programs = [
            (
                "Urban Forestry",
                "Implementing urban and rural greening initiatives, restoring public parks, promoting biodiversity, and encouraging climate-resilient ecosystems.",
            ),
            (
                "Skill Development",
                "Partnering with training institutions and industries to provide youth with employable skills and decent work opportunities.",
            ),
            (
                "Generic Medicines",
                "Facilitating health camps, awareness programmes, and initiatives to improve access to affordable healthcare and generic medicines.",
            ),
            (
                "Education and Financial Aid",
                "Supporting educational advancement through scholarships, mentorship, and financial assistance for students from disadvantaged backgrounds.",
            ),
            (
                "Legal Awareness and Civic Engagement",
                "Promoting awareness on rights, entitlements, and governance to empower citizens, especially marginalized groups.",
            ),
            (
                "Sustainable Plastic Waste Management",
                "Creating awareness and building systems for effective plastic waste collection, segregation, and recycling.",
            ),
            (
                "Strengthening Farmer Producer Organizations (FPOs)",
                "Supporting FPOs with training, infrastructure, and market linkages to enhance agricultural productivity and fair incomes.",
            ),
        ]
        if not Program.objects.exists():
            for i, (title, desc) in enumerate(programs):
                Program.objects.create(
                    title=title,
                    short_description=desc,
                    description=desc,
                    order=i,
                    meta_title=f"{title} | Vaaradhi Trust",
                    meta_description=desc[:160],
                )

        if not Project.objects.exists():
            Project.objects.create(
                title="Empowering Youth for Careers in Hospitality",
                category="Skill Development",
                status=Project.STATUS_ACTIVE,
                summary="Hospitality skill pathways for youth through institutional collaboration.",
                is_featured=True,
                order=0,
            )
            Project.objects.create(
                title="Awareness on Generic Medicines",
                category="Public Health",
                status=Project.STATUS_ACTIVE,
                summary="Community awareness and stakeholder engagement on affordable generic medicines.",
                is_featured=True,
                order=1,
            )
            Project.objects.create(
                title="Empowering Unemployed Youth Through Construction Skills",
                category="Skill Development",
                status=Project.STATUS_ACTIVE,
                summary="Construction skill development in collaboration with National Academy of Construction.",
                partner_name="National Academy of Construction",
                is_featured=True,
                order=2,
            )
            Project.objects.create(
                title="Ongoing Skill Development Project with NAC",
                category="Skill Development",
                status=Project.STATUS_ONGOING,
                summary="Ongoing collaboration with NAC for specialised construction skill courses.",
                partner_name="National Academy of Construction",
                order=3,
            )

        if not Initiative.objects.exists():
            Initiative.objects.create(
                title="Skill Development for Youth",
                short_description="Industry-relevant training and pathways to dignified employment.",
                description="Vaaradhi Trust partners with training institutions to equip youth with employable skills.",
                order=0,
            )
            Initiative.objects.create(
                title="Urban Forestry & Climate Action",
                short_description="Community-led greening to restore ecosystems and cool cities.",
                order=1,
            )
            Initiative.objects.create(
                title="Public Health & Generic Medicines",
                short_description="Improving awareness and access to affordable healthcare.",
                order=2,
            )
            Initiative.objects.create(
                title="Education & Financial Aid",
                short_description="Scholarships and mentorship for students from disadvantaged backgrounds.",
                order=3,
            )

        if not Event.objects.exists():
            Event.objects.create(
                title="TISS Conclave",
                event_type="TISS Conclave",
                summary="Engagement on policy, youth leadership, and community development themes.",
                is_featured=True,
            )
            Event.objects.create(
                title="Doctors' Conclave 1",
                event_type="Doctors' Conclave",
                summary="Dialogue with medical professionals on public health and medicine access.",
                is_featured=True,
            )
            Event.objects.create(
                title="Regular Community Events",
                event_type="Regular Events",
                summary="Ongoing community sessions, field visits, and awareness drives.",
            )

        if not MediaItem.objects.exists():
            MediaItem.objects.create(
                title="Meeting with Prof. Aseem Prakash on student engagement opportunities",
                excerpt="Exploring Capstone Projects, Fieldwork, and Advocacy Internships with School of Public Policy and Governance.",
                published_at=timezone.now().date(),
            )
            MediaItem.objects.create(
                title="MoU Exchange with National Academy of Construction (NAC)",
                excerpt="Empowering youth and workers through specialised construction skill development courses.",
                published_at=timezone.now().date(),
            )
            MediaItem.objects.create(
                title="MOU with Voon Hands Foundation on Urban Forestry",
                excerpt="Collaboration related to urban forestry and tackling monkey menace at Narsapur Urban Forest range.",
                published_at=timezone.now().date(),
            )

        if not Partner.objects.exists():
            for i, (name, ptype, brief) in enumerate(
                [
                    ("National Academy of Construction", "academic", "Skill development collaboration for construction trades."),
                    ("Voon Hands Foundation", "ngo", "Urban forestry partnership at Narsapur."),
                    ("Institute of Hotel Management, Shri Shakti", "academic", "Hospitality skill development exploration."),
                    ("Lorven Pharma and Surgicals", "csr", "Dialogue on PMBJP operational issues and public impact."),
                ]
            ):
                Partner.objects.create(name=name, partner_type=ptype, brief=brief, order=i)

        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                name="Community Participant",
                role_type="beneficiary",
                role_label="Skill Development Cohort",
                quote="The training opened a pathway I did not think was possible. I gained confidence and a clear direction for work.",
                order=0,
            )
            Testimonial.objects.create(
                name="Institution Partner",
                role_type="stakeholder",
                role_label="Training Partner",
                quote="Vaaradhi Trust brings clarity, purpose, and strong on-ground coordination to every collaboration.",
                order=1,
            )
            Testimonial.objects.create(
                name="Programme Supporter",
                role_type="donor",
                role_label="Donor",
                quote="Supporting Vaaradhi means investing in practical solutions that connect resources to people who need them most.",
                order=2,
            )

        if not TeamMember.objects.exists():
            TeamMember.objects.create(
                name="Subbarao Kattamuri",
                designation="Founder",
                category=TeamMember.CATEGORY_BOARD,
                bio="Founder of Vaaradhi Trust, dedicated to bridging surplus with unmet need through purposeful social action.",
                order=0,
            )

        if not GovernanceDocument.objects.exists():
            GovernanceDocument.objects.create(
                title="Registration & Regulatory Disclosures",
                description="Key registration certificates and approvals will be uploaded as they are issued.",
                year=2025,
            )

        from django.core.files import File
        from pathlib import Path

        media_campaigns = Path(__file__).resolve().parents[3] / "media" / "campaigns"
        cause_defs = [
            (
                "Urban Forestry and Climate Action",
                "urban-forestry-and-climate-action",
                "Adopt and nurture trees over a three-year care cycle that cools cities and restores ecosystems.",
                "forestry.png",
                0,
            ),
            (
                "Skill Development and Employment Generation",
                "skill-development-and-employment-generation",
                "Fund training seats that lead to certified jobs and dignified livelihoods for youth.",
                "skills.png",
                1,
            ),
            (
                "Generics for All Initiative",
                "generics-for-all-initiative",
                "Help families access affordable generic medicines through awareness and sustained support.",
                "health.png",
                2,
            ),
            (
                "Plastic Waste Management",
                "plastic-waste-management",
                "Build community systems for collection, segregation, and responsible recycling.",
                "plastic.png",
                3,
            ),
            (
                "Farmer Producer Organizations",
                "farmer-producer-organizations",
                "Strengthen FPOs with training, infrastructure, and fair market linkages.",
                "fpo.png",
                4,
            ),
            (
                "Education and Financial Aid",
                "education-and-financial-aid",
                "Support scholarships, mentorship, and educational advancement for students in need.",
                "education.png",
                5,
            ),
            (
                "Legal Awareness and Civic Engagement",
                "legal-awareness-and-civic-engagement",
                "Empower citizens with awareness of rights, entitlements, and civic participation.",
                "legal.png",
                6,
            ),
        ]

        for title, slug, summary, filename, order in cause_defs:
            obj, created = DonationCampaign.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "summary": summary,
                    "description": summary,
                    "is_featured": True,
                    "is_active": True,
                    "order": order,
                    "donate_url": f"/donate/?cause={slug}",
                },
            )
            img_path = media_campaigns / filename
            if img_path.exists() and (created or not obj.image):
                with img_path.open("rb") as fh:
                    obj.image.save(filename, File(fh), save=True)

        # Soft-remove older demo campaigns that are not in the official cause list
        keep_slugs = [c[1] for c in cause_defs]
        DonationCampaign.objects.exclude(slug__in=keep_slugs).update(is_active=False)

        # Attach who-we-are media if missing
        who_path = Path(__file__).resolve().parents[3] / "media" / "home" / "who-we-are.png"
        if who_path.exists() and not site.who_we_are_media:
            with who_path.open("rb") as fh:
                site.who_we_are_media.save("who-we-are.png", File(fh), save=True)
                site.who_we_are_media_is_video = False
                site.save()

        Career.objects.get_or_create(
            slug="programme-coordinator",
            defaults={
                "title": "Programme Coordinator",
                "location": "Hyderabad",
                "employment_type": "Full-time",
                "summary": "Coordinate on-ground implementation across skill development and community programmes.",
                "description": "We will add detailed JD and vacancies as roles open. Express interest anytime at contact@vaaradhi.org.in.",
                "is_open": False,
            },
        )

        self.stdout.write(self.style.SUCCESS("Vaaradhi Trust content seeded successfully."))
