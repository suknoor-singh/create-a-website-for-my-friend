from django.contrib import admin

from home.models import ContactInquiry, GoogleReview, GoogleReviewFeed, NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at", "last_emailed_at")
    list_filter = ("is_active",)
    search_fields = ("email",)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_resolved")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("name", "email", "phone", "message")


class GoogleReviewInline(admin.TabularInline):
    model = GoogleReview
    extra = 0
    readonly_fields = (
        "author_name",
        "rating",
        "relative_publish_time_description",
        "review_text",
        "review_url",
    )


@admin.register(GoogleReviewFeed)
class GoogleReviewFeedAdmin(admin.ModelAdmin):
    list_display = ("place_name", "average_rating", "total_review_count", "last_synced_at")
    readonly_fields = ("last_synced_at", "sync_error")
    inlines = [GoogleReviewInline]
