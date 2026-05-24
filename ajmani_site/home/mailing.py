from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from home.models import NewsletterSubscriber


def send_contact_inquiry_notification(inquiry, recipient_email):
    if not recipient_email:
        return

    subject = f"New website enquiry from {inquiry.name}"
    body = render_to_string(
        "home/emails/contact_inquiry.txt",
        {
            "inquiry": inquiry,
        },
    )
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
        reply_to=[inquiry.email],
    )
    message.send(fail_silently=False)


def send_newsletter_issue_to_subscribers(issue):
    recipients = list(
        NewsletterSubscriber.objects.filter(is_active=True).values_list("email", flat=True)
    )
    if not recipients:
        return 0

    issue_url = f"{settings.WAGTAILADMIN_BASE_URL.rstrip('/')}{issue.get_url()}"
    html_body = render_to_string(
        "insights/emails/newsletter_issue.html",
        {
            "issue": issue,
            "issue_url": issue_url,
        },
    )
    text_body = render_to_string(
        "insights/emails/newsletter_issue.txt",
        {
            "issue": issue,
            "issue_url": issue_url,
            "plain_summary": strip_tags(issue.body),
        },
    )

    sent_count = 0
    for email in recipients:
        message = EmailMultiAlternatives(
            subject=issue.email_subject_override or issue.title,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)
        sent_count += 1

    NewsletterSubscriber.objects.filter(is_active=True).update(last_emailed_at=timezone.now())
    return sent_count
