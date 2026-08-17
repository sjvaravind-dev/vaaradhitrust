from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Singleton site configuration."""

    org_name = models.CharField(max_length=120, default="Vaaradhi Trust")
    tagline = models.CharField(
        max_length=200, default="Bridging Communities With Care"
    )
    phone = models.CharField(max_length=40, default="+91 7674996876")
    email = models.EmailField(default="contact@vaaradhi.org.in")
    address = models.TextField(
        default=(
            "Vaaradhi Trust, GV Chamber, 7-2-C8 & C8/2, "
            "IDA Sanath Nagar, Hyderabad – 500018, Telangana, India"
        )
    )
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(
        default="https://www.linkedin.com/company/vaaradhi-trust/"
    )
    events_linkedin_url = models.URLField(
        blank=True,
        help_text="Events section redirects here when set.",
    )
    donate_url = models.CharField(max_length=255, default="/donate/")
    volunteer_url = models.CharField(max_length=255, default="/join-us/volunteer/")
    logo = models.ImageField(upload_to="brand/", blank=True, null=True)
    footer_about = models.TextField(
        blank=True,
        default=(
            "Vaaradhi Trust is a non-profit dedicated to advancing inclusive "
            "and sustainable development through high-impact programs."
        ),
    )
    # Who we are (home static block)
    who_we_are_title = models.CharField(max_length=160, default="Who are we?")
    who_we_are_text = models.TextField(
        blank=True,
        default=(
            "Vaaradhi Trust is a non-profit organization dedicated to advancing "
            "inclusive and sustainable development through high-impact programs. "
            "We serve as a bridge between communities, governments, and "
            "corporations—connecting resources, expertise, and intent to create "
            "meaningful social and environmental change."
        ),
    )
    who_we_are_media = models.FileField(
        upload_to="home/", blank=True, null=True, help_text="Photo or video"
    )
    who_we_are_media_is_video = models.BooleanField(default=False)
    vision = models.TextField(
        default=(
            "To build a resilient and equitable society where every individual "
            "and community has the opportunity to thrive with dignity."
        )
    )
    mission = models.TextField(
        default=(
            "To bridge communities with care by connecting surplus resources, "
            "expertise, and intent to unmet needs through collaborative, "
            "high-impact social and environmental initiatives."
        )
    )
    story_quote = models.CharField(
        max_length=300,
        default="The world has enough for everyone's need, but not everyone's greed.",
    )
    story_quote_author = models.CharField(max_length=120, default="Mahatma Gandhi")
    story_body = models.TextField(blank=True)
    privacy_policy = models.TextField(blank=True)
    volunteer_content = models.TextField(blank=True)
    csr_content = models.TextField(blank=True)
    meta_title = models.CharField(
        max_length=70, default="Vaaradhi Trust | Bridging Communities With Care"
    )
    meta_description = models.CharField(
        max_length=170,
        default=(
            "Vaaradhi Trust advances inclusive development through skill "
            "development, urban forestry, public health, education and community programmes in Telangana."
        ),
    )
    meta_keywords = models.CharField(
        max_length=255,
        default="Vaaradhi Trust, NGO Hyderabad, skill development, urban forestry, public health",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.org_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ScrollingNews(TimeStampedModel):
    text = models.CharField(max_length=300)
    link = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Scrolling News"

    def __str__(self):
        return self.text[:60]


class PopupBanner(TimeStampedModel):
    title = models.CharField(max_length=160)
    image = models.ImageField(upload_to="popups/")
    link = models.CharField(max_length=255, blank=True)
    button_text = models.CharField(max_length=60, blank=True, default="Learn More")
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class HomeSlider(TimeStampedModel):
    THEME_CHOICES = [
        ("skills", "Skill Development"),
        ("careers", "Creating Careers"),
        ("youth", "Empowering Youth"),
        ("green", "Greening Cities"),
        ("futures", "Securing Futures"),
        ("health", "Health Equity"),
        ("community", "For Every Community"),
        ("custom", "Custom"),
    ]
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=255, blank=True)
    theme = models.CharField(max_length=40, choices=THEME_CHOICES, default="custom")
    background_image = models.ImageField(upload_to="sliders/", blank=True, null=True)
    cta_text = models.CharField(max_length=60, blank=True, default="Explore")
    cta_link = models.CharField(max_length=255, blank=True)
    overlay_color = models.CharField(
        max_length=30, blank=True, default="rgba(10, 52, 40, 0.55)"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class ImpactStat(TimeStampedModel):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=40, help_text="e.g. 15100+, 7, Telangana")
    icon = models.CharField(
        max_length=40, blank=True, default="impact", help_text="CSS icon key"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.value} {self.label}"


class Initiative(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="initiatives/", blank=True, null=True)
    donate_link = models.CharField(max_length=255, blank=True, default="/donate/")
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("initiative_detail", kwargs={"slug": self.slug})


class Program(TimeStampedModel):
    """Focus areas / objectives (Urban Forestry, Skills, etc.)."""

    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    description = models.TextField(blank=True)
    icon_key = models.CharField(max_length=40, blank=True, default="leaf")
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=170, blank=True)

    class Meta:
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"slug": self.slug})


class Project(TimeStampedModel):
    STATUS_ACTIVE = "active"
    STATUS_ONGOING = "ongoing"
    STATUS_UPCOMING = "upcoming"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_UPCOMING, "Upcoming"),
        (STATUS_COMPLETED, "Completed"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=80, blank=True)
    program = models.ForeignKey(
        Program, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    summary = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    partner_name = models.CharField(max_length=160, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})


class Event(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    event_type = models.CharField(
        max_length=80,
        blank=True,
        help_text="e.g. TISS Conclave, Doctors' Conclave, Regular Event",
    )
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    event_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    external_url = models.URLField(
        blank=True, help_text="Optional LinkedIn or external link"
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-event_date", "order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MediaItem(TimeStampedModel):
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="media_news/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    published_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=170, blank=True)

    class Meta:
        ordering = ["-published_at", "order"]
        verbose_name = "Media / News"
        verbose_name_plural = "Media & News"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("media_detail", kwargs={"slug": self.slug})


class Partner(TimeStampedModel):
    TYPE_DONOR = "donor"
    TYPE_NGO = "ngo"
    TYPE_GOVT = "government"
    TYPE_CSR = "csr"
    TYPE_ACADEMIC = "academic"
    TYPE_OTHER = "other"
    TYPE_CHOICES = [
        (TYPE_DONOR, "Donor"),
        (TYPE_NGO, "NGO"),
        (TYPE_GOVT, "Government"),
        (TYPE_CSR, "CSR / Corporate"),
        (TYPE_ACADEMIC, "Academic"),
        (TYPE_OTHER, "Other"),
    ]
    name = models.CharField(max_length=160)
    partner_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_CSR)
    logo = models.ImageField(upload_to="partners/", blank=True, null=True)
    brief = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Testimonial(TimeStampedModel):
    ROLE_BENEFICIARY = "beneficiary"
    ROLE_DONOR = "donor"
    ROLE_INTERN = "intern"
    ROLE_EMPLOYEE = "employee"
    ROLE_STAKEHOLDER = "stakeholder"
    ROLE_CHOICES = [
        (ROLE_BENEFICIARY, "Beneficiary"),
        (ROLE_DONOR, "Donor"),
        (ROLE_INTERN, "Intern"),
        (ROLE_EMPLOYEE, "Employee"),
        (ROLE_STAKEHOLDER, "Stakeholder"),
    ]
    name = models.CharField(max_length=120)
    role_label = models.CharField(max_length=120, blank=True)
    role_type = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=ROLE_BENEFICIARY
    )
    quote = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.role_type})"


class TeamMember(TimeStampedModel):
    CATEGORY_BOARD = "board"
    CATEGORY_TEAM = "team"
    CATEGORY_ADVISOR = "advisor"
    CATEGORY_CHOICES = [
        (CATEGORY_BOARD, "Board"),
        (CATEGORY_TEAM, "Team"),
        (CATEGORY_ADVISOR, "Advisor"),
    ]
    name = models.CharField(max_length=120)
    designation = models.CharField(max_length=160)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_TEAM
    )
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} — {self.designation}"


class GovernanceDocument(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="governance/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year"]

    def __str__(self):
        return self.title


class Career(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=120, blank=True, default="Hyderabad")
    employment_type = models.CharField(max_length=60, blank=True, default="Full-time")
    summary = models.TextField()
    description = models.TextField(blank=True)
    apply_email = models.EmailField(blank=True, default="contact@vaaradhi.org.in")
    apply_url = models.URLField(blank=True)
    is_open = models.BooleanField(default=True)
    posted_at = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-posted_at", "order"]
        verbose_name_plural = "Careers / Vacancies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DonationCampaign(TimeStampedModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="campaigns/", blank=True, null=True)
    goal_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    raised_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    donate_url = models.CharField(max_length=255, blank=True, default="/donate/")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Donation(TimeStampedModel):
    TYPE_ONE_TIME = "one-time"
    TYPE_MONTHLY = "monthly"
    TYPE_CHOICES = [
        (TYPE_ONE_TIME, "One-time"),
        (TYPE_MONTHLY, "Monthly"),
    ]
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    pan = models.CharField(max_length=10, blank=True)
    cause_slug = models.SlugField(max_length=80)
    cause_title = models.CharField(max_length=180)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="INR")
    donation_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_ONE_TIME
    )
    send_updates = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    campaign = models.ForeignKey(
        DonationCampaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    razorpay_order_id = models.CharField(max_length=80, blank=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=80, blank=True, db_index=True)
    razorpay_subscription_id = models.CharField(max_length=80, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · ₹{self.amount} · {self.cause_title} ({self.status})"

    @property
    def amount_paise(self):
        return int(self.amount * 100)


class PageHit(models.Model):
    """Lightweight traffic counter for admin insight."""

    path = models.CharField(max_length=255, db_index=True)
    hits = models.PositiveIntegerField(default=0)
    last_hit = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["path"])]

    def __str__(self):
        return f"{self.path} ({self.hits})"
