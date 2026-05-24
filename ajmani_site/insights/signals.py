from django.dispatch import receiver
from django.utils import timezone
from wagtail.signals import page_published

from home.mailing import send_newsletter_issue_to_subscribers
from insights.models import NewsletterPage


@receiver(page_published, sender=NewsletterPage)
def send_newsletter_notifications_on_publish(sender, instance, **kwargs):
    if not instance.send_to_subscribers_on_publish or instance.notification_sent_at:
        return

    send_newsletter_issue_to_subscribers(instance)
    NewsletterPage.objects.filter(pk=instance.pk).update(notification_sent_at=timezone.now())
