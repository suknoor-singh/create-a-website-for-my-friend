# Lalit workflow guide

## How Lalit updates the website

1. Open the Wagtail admin at `/admin/`.
2. Sign in with the editor account you create for him.
3. Open the `Home` page to update:
   - hero title and intro
   - phone, email, office address
   - practice areas
   - compliance note
   - WhatsApp message
   - Google Maps and review configuration fields
4. Publish the page after edits.

## How the page structure now works

The site is no longer just a single homepage. It now has these editable sections under `Pages`:

- `Home`
- `About Us`
- `Expertise`
- `Blog`
- `Contact`
- `Newsletter Archive`

For `About Us` and `Expertise`, each child page opens as its own proper page from the menu, similar to the reference site you shared.

## How junior teammates can edit only the blog

The cleanest approach is to give junior teammates access only to the `Blog` section in Wagtail.

1. Open `/admin/groups/`.
2. Create a group such as `Blog Editors`.
3. Add page permissions for the `Blog` parent page:
   - `Add`
   - `Edit`
   - `Publish`
   - `Lock`
4. Assign junior user accounts to that group.
5. Do not give that group permissions on `Home`, `About Us`, `Expertise`, or `Contact`.

This works well because the blog now lives in its own page subtree.

If you want a tighter workflow, publish rights can be removed from juniors and kept only with Lalit or a senior editor.

## How Lalit publishes a newsletter

1. In Wagtail admin, open `Pages`.
2. Open `Newsletters`.
3. Add a new `Newsletter Page`.
4. Fill in:
   - title
   - publication date
   - issue label
   - summary
   - optional PDF document
   - body
5. Keep `Send to subscribers on publish` enabled.
6. Publish the page.

When SMTP or SES is configured, the first publish sends that issue to active subscribers automatically.

If you already have a finished PDF version of the newsletter, upload it to the `PDF document` field on the newsletter page. The archive and issue page will automatically show an `Open PDF` button.

## How the blog works

1. In Wagtail admin, open `Pages`.
2. Open `Blog`.
3. Add a new `Blog Page`.
4. Fill in:
   - title
   - publication date
   - summary
   - author name
   - body
5. Publish the page.

This is separate from the newsletter archive. That separation makes permissions cleaner for junior team members.

## How newsletter signup works

- Website visitors can enter their email in the newsletter section.
- Their email is stored in the database in `NewsletterSubscriber`.
- When a newsletter is published, active subscribers are emailed one by one.

## How contact enquiries work

- Website visitors submit the contact form in the contact section.
- Each enquiry is stored in the database in `ContactInquiry`.
- If email is configured, the site also sends the enquiry to `lalit@ajmaniandlawpartners.com`.

## How to configure outgoing email

For local development you can keep the default console email backend.

For real delivery, set these environment variables:

```powershell
$env:EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST="email-smtp.ap-south-1.amazonaws.com"
$env:EMAIL_PORT="587"
$env:EMAIL_HOST_USER="YOUR_SMTP_USERNAME"
$env:EMAIL_HOST_PASSWORD="YOUR_SMTP_PASSWORD"
$env:EMAIL_USE_TLS="true"
$env:DEFAULT_FROM_EMAIL="lalit@ajmaniandlawpartners.com"
$env:WAGTAILADMIN_BASE_URL="https://ajmaniandlawpartners.com"
```

If you use Amazon SES, verify the sender domain or email first.

## How to enable dynamic Google reviews

The site now supports an official Google-backed dynamic review path, but it needs a Google Places API key.

Set:

```powershell
$env:GOOGLE_PLACES_API_KEY="YOUR_GOOGLE_PLACES_API_KEY"
```

Notes:

- This pulls a limited set of live reviews, enough for the homepage cards.
- Exact all-review sync from Google requires the Google Business Profile API and verified business access.
- Without the API key, the site falls back to the seeded review cards.
