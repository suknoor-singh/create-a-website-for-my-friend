from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from home.forms import ContactInquiryForm, NewsletterSignupForm
from home.mailing import send_contact_inquiry_notification
from home.models import ContactInquiry, HomePage, NewsletterSubscriber


def _home_redirect(anchor):
    homepage = HomePage.objects.first()
    target = homepage.url if homepage else "/"
    return redirect(f"{target}#{anchor}")


@require_POST
def submit_inquiry(request):
    form = ContactInquiryForm(request.POST)
    homepage = HomePage.objects.first()

    if not form.is_valid():
        messages.error(request, "Please complete the contact form with a valid name, email, and message.")
        return _home_redirect("contact")

    inquiry = ContactInquiry.objects.create(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
        phone=form.cleaned_data.get("phone", ""),
        message=form.cleaned_data["message"],
    )

    try:
        send_contact_inquiry_notification(inquiry, homepage.contact_email if homepage else "")
    except Exception:
        messages.warning(
            request,
            "Your enquiry was saved, but email delivery is not configured yet. Please finish SMTP or SES setup.",
        )
    else:
        messages.success(request, "Your enquiry has been sent. Ajmani and Law Partners can reply directly to your email.")

    return _home_redirect("contact")


@require_POST
def subscribe_newsletter(request):
    form = NewsletterSignupForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please enter a valid email address to subscribe.")
        return _home_redirect("newsletters")

    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=form.cleaned_data["email"],
        defaults={"is_active": True},
    )
    if not created and not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save(update_fields=["is_active", "updated_at"])

    messages.success(request, "Subscription saved. Future published newsletters can be delivered to this email.")
    return _home_redirect("newsletters")
