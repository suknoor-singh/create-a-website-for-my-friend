from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.documents import get_document_model_string
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class NewsletterIndexPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["insights.NewsletterPage"]

    intro = models.TextField(
        blank=True,
        default=(
            "A running archive of monthly newsletters covering legal updates, litigation trends, "
            "and concise client-facing commentary."
        ),
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["newsletters"] = NewsletterPage.objects.child_of(self).live().public().order_by("-publication_date")
        return context


class NewsletterPage(Page):
    parent_page_types = ["insights.NewsletterIndexPage"]
    subpage_types = []

    publication_date = models.DateField("Publication date")
    issue_label = models.CharField(
        max_length=80,
        blank=True,
        help_text="Examples: May 2026 issue, Volume 1 Issue 3.",
    )
    summary = models.TextField(max_length=260, blank=True)
    email_subject_override = models.CharField(max_length=150, blank=True)
    send_to_subscribers_on_publish = models.BooleanField(
        default=True,
        help_text="When this issue is published for the first time, send it to active newsletter subscribers.",
    )
    notification_sent_at = models.DateTimeField(null=True, blank=True, editable=False)
    pdf_document = models.ForeignKey(
        get_document_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional PDF version of this newsletter issue for direct download or reading.",
    )
    body = RichTextField(features=["h2", "h3", "bold", "italic", "link", "ol", "ul", "document-link"])

    search_fields = Page.search_fields + [
        index.SearchField("summary"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("issue_label"),
        FieldPanel("summary"),
        FieldPanel("email_subject_override"),
        FieldPanel("send_to_subscribers_on_publish"),
        FieldPanel("pdf_document"),
        FieldPanel("body"),
    ]

    class Meta:
        ordering = ["-publication_date"]
