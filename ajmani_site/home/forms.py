from django import forms


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Type your email",
                "aria-label": "Email address",
            }
        )
    )


class ContactInquiryForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name",
                "aria-label": "Your name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email",
                "aria-label": "Your email",
            }
        )
    )
    phone = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone number",
                "aria-label": "Phone number",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Explain your matter briefly",
                "rows": 6,
                "aria-label": "Explain your matter briefly",
            }
        )
    )
