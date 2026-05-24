from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.search import index


class PracticeAreaBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=90)
    description = blocks.TextBlock(required=True, max_length=260)


class CourtBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, max_length=90)
    detail = blocks.TextBlock(required=True, max_length=200)


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True, max_length=320)
    author = blocks.CharBlock(required=True, max_length=120)
    rating = blocks.IntegerBlock(required=True, min_value=1, max_value=5, default=5)
    source = blocks.CharBlock(required=True, max_length=60, default="Google Reviews")


class HomePage(Page):
    max_count = 1
    subpage_types = [
        "home.SectionIndexPage",
        "home.ContactPage",
        "home.BlogIndexPage",
        "insights.NewsletterIndexPage",
    ]

    intro_kicker = models.CharField(
        max_length=80,
        default="Delhi Litigation Counsel",
        help_text="Short line above the main headline.",
    )
    hero_title = models.CharField(
        max_length=140,
        default="Trusted representation across Delhi district, high and supreme courts.",
    )
    hero_subtitle = models.TextField(
        default=(
            "Ajmani and Law Partners helps individuals, families, and businesses navigate "
            "complex disputes with clear advice, responsive counsel, and disciplined courtroom strategy."
        )
    )
    primary_cta_label = models.CharField(max_length=40, default="Book a consultation")
    primary_cta_link = models.CharField(
        max_length=255,
        default="#contact",
        help_text="Use a full URL or an in-page anchor such as #contact.",
    )
    secondary_cta_label = models.CharField(max_length=40, default="Read newsletters")
    secondary_cta_link = models.CharField(max_length=255, default="#newsletters")

    credibility_points = StreamField(
        [("point", blocks.CharBlock(max_length=90))],
        use_json_field=True,
        blank=True,
        help_text="Short trust markers shown below the hero section.",
    )
    firm_overview_title = models.CharField(max_length=90, default="A litigation-first firm for Delhi matters")
    firm_overview = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ol", "ul"],
        default=(
            "<p>Ajmani and Law Partners combines trial-readiness with practical guidance. "
            "The firm is positioned to represent clients in district courts, the Delhi High Court, "
            "and the Supreme Court of India while keeping communication direct and client-focused.</p>"
        ),
    )
    founder_name = models.CharField(max_length=120, default="Advocate Ajmani")
    founder_designation = models.CharField(max_length=120, default="Founding Partner")
    founder_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    founder_linkedin_url = models.URLField(blank=True)
    founder_bio = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ol", "ul"],
        default=(
            "<p>Share the founder's courtroom experience, notable appearances, sector knowledge, "
            "and the kind of matters the firm is best known for.</p>"
        ),
    )
    founder_highlights = StreamField(
        [("highlight", blocks.CharBlock(max_length=100))],
        use_json_field=True,
        blank=True,
        help_text="Examples: Client-first communication, Trial strategy, Strong briefing discipline.",
    )
    court_coverage = StreamField(
        [("court", CourtBlock())],
        use_json_field=True,
        blank=True,
    )
    practice_areas = StreamField(
        [("practice", PracticeAreaBlock())],
        use_json_field=True,
        blank=True,
    )
    testimonials = StreamField(
        [("testimonial", TestimonialBlock())],
        use_json_field=True,
        blank=True,
    )
    newsletter_title = models.CharField(max_length=90, default="Monthly legal newsletters")
    newsletter_intro = models.TextField(
        default=(
            "Publish short, useful updates on new judgments, procedural changes, and practical legal takeaways."
        )
    )
    google_reviews_query = models.CharField(max_length=255, blank=True)
    google_place_id = models.CharField(max_length=180, blank=True)
    google_business_share_url = models.URLField(blank=True)
    google_maps_url = models.URLField(blank=True)
    google_maps_embed_query = models.CharField(max_length=255, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    whatsapp_default_message = models.TextField(
        blank=True,
        default="Hello, I would like to discuss a legal matter with Ajmani and Law Partners.",
    )
    contact_phone = models.CharField(max_length=40, blank=True)
    contact_email = models.EmailField(blank=True)
    office_address = models.TextField(blank=True)
    compliance_note = models.TextField(
        default=(
            "This website is intended for informational purposes and does not create an advocate-client relationship."
        )
    )

    search_fields = Page.search_fields + [
        index.SearchField("hero_title"),
        index.SearchField("hero_subtitle"),
        index.SearchField("firm_overview"),
        index.SearchField("founder_bio"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("intro_kicker"),
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("primary_cta_label"),
                FieldPanel("primary_cta_link"),
                FieldPanel("secondary_cta_label"),
                FieldPanel("secondary_cta_link"),
            ],
            heading="Hero section",
        ),
        FieldPanel("credibility_points"),
        MultiFieldPanel(
            [
                FieldPanel("firm_overview_title"),
                FieldPanel("firm_overview"),
                FieldPanel("founder_name"),
                FieldPanel("founder_designation"),
                FieldPanel("founder_image"),
                FieldPanel("founder_linkedin_url"),
                FieldPanel("founder_bio"),
                FieldPanel("founder_highlights"),
            ],
            heading="Firm profile",
        ),
        FieldPanel("court_coverage"),
        FieldPanel("practice_areas"),
        FieldPanel("testimonials"),
        MultiFieldPanel(
            [
                FieldPanel("newsletter_title"),
                FieldPanel("newsletter_intro"),
            ],
            heading="Newsletter section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("google_reviews_query"),
                FieldPanel("google_place_id"),
                FieldPanel("google_business_share_url"),
                FieldPanel("google_maps_url"),
                FieldPanel("google_maps_embed_query"),
                FieldPanel("whatsapp_number"),
                FieldPanel("whatsapp_default_message"),
            ],
            heading="Integrations",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_phone"),
                FieldPanel("contact_email"),
                FieldPanel("office_address"),
                FieldPanel("compliance_note"),
            ],
            heading="Contact and compliance",
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        from home.forms import ContactInquiryForm, NewsletterSignupForm
        from home.google_reviews import get_google_review_context
        from insights.models import NewsletterIndexPage, NewsletterPage

        context["latest_newsletters"] = NewsletterPage.objects.live().public().order_by("-publication_date")[:3]
        context["latest_blog_posts"] = BlogPage.objects.live().public().order_by("-publication_date")[:3]
        newsletter_index = (
            self.get_children()
            .type(NewsletterIndexPage)
            .live()
            .public()
            .first()
        )
        context["newsletter_index"] = newsletter_index.specific if newsletter_index else None
        feed, google_reviews = get_google_review_context(self)
        context["google_review_feed"] = feed
        context["google_reviews"] = google_reviews
        context["newsletter_form"] = NewsletterSignupForm()
        context["contact_form"] = ContactInquiryForm()
        return context


class SectionIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.StandardContentPage"]

    intro = models.TextField(
        blank=True,
        help_text="Short introduction shown near the top of the page.",
    )
    body = RichTextField(
        blank=True,
        features=["h2", "h3", "bold", "italic", "link", "ol", "ul"],
        help_text="Optional overview content for this section landing page.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Section index page"
        verbose_name_plural = "Section index pages"

    def get_context(self, request):
        context = super().get_context(request)
        context["child_pages"] = self.get_children().live().public().specific()
        return context


class StandardContentPage(Page):
    parent_page_types = ["home.SectionIndexPage"]
    subpage_types = []

    intro = models.TextField(blank=True, max_length=320)
    featured_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = RichTextField(features=["h2", "h3", "bold", "italic", "link", "ol", "ul", "document-link"])
    highlights = StreamField(
        [("highlight", blocks.CharBlock(max_length=110))],
        use_json_field=True,
        blank=True,
        help_text="Optional bullet points for the side panel.",
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("featured_image"),
        FieldPanel("body"),
        FieldPanel("highlights"),
    ]

    class Meta:
        verbose_name = "Content page"
        verbose_name_plural = "Content pages"


class ContactPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    intro = models.TextField(
        blank=True,
        default="Reach out for consultations, updates on an existing matter, or general questions about the firm's services.",
    )
    body = RichTextField(
        blank=True,
        features=["h2", "h3", "bold", "italic", "link", "ol", "ul"],
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Contact page"
        verbose_name_plural = "Contact pages"

    def get_context(self, request):
        context = super().get_context(request)
        from home.forms import ContactInquiryForm

        context["root_page"] = self.get_site().root_page.specific
        context["contact_form"] = ContactInquiryForm()
        return context


class BlogIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.BlogPage"]

    intro = models.TextField(
        blank=True,
        default="Articles, legal explainers, case-note style commentary, and practical writing from Ajmani and Law Partners.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    class Meta:
        verbose_name = "Blog index page"
        verbose_name_plural = "Blog index pages"

    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = BlogPage.objects.child_of(self).live().public().order_by("-publication_date")
        return context


class BlogPage(Page):
    parent_page_types = ["home.BlogIndexPage"]
    subpage_types = []

    publication_date = models.DateField("Publication date")
    summary = models.TextField(max_length=280, blank=True)
    author_name = models.CharField(max_length=120, blank=True, help_text="Example: Editorial Team or a junior associate.")
    body = RichTextField(features=["h2", "h3", "bold", "italic", "link", "ol", "ul", "document-link"])

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("author_name"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("summary"),
        FieldPanel("author_name"),
        FieldPanel("body"),
    ]

    class Meta:
        ordering = ["-publication_date"]
        verbose_name = "Blog page"
        verbose_name_plural = "Blog pages"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_emailed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class ContactInquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Contact inquiries"

    def __str__(self):
        return f"{self.name} - {self.email}"


class GoogleReviewFeed(models.Model):
    key = models.CharField(max_length=80, unique=True, default="ajmani-homepage")
    place_id = models.CharField(max_length=180, blank=True)
    place_name = models.CharField(max_length=255, blank=True)
    average_rating = models.FloatField(default=0)
    total_review_count = models.PositiveIntegerField(default=0)
    google_maps_url = models.URLField(blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    sync_error = models.TextField(blank=True)

    class Meta:
        verbose_name = "Google review feed"
        verbose_name_plural = "Google review feeds"

    def __str__(self):
        return self.place_name or self.key


class GoogleReview(models.Model):
    feed = models.ForeignKey(GoogleReviewFeed, on_delete=models.CASCADE, related_name="reviews")
    review_id = models.CharField(max_length=255, unique=True)
    author_name = models.CharField(max_length=255)
    author_url = models.URLField(blank=True)
    author_photo_url = models.URLField(blank=True)
    rating = models.FloatField(default=0)
    relative_publish_time_description = models.CharField(max_length=120, blank=True)
    review_text = models.TextField(blank=True)
    review_url = models.URLField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-published_at", "-id"]

    def __str__(self):
        return f"{self.author_name} ({self.rating})"
