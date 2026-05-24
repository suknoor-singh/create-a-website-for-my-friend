# Ajmani and Law Partners Website

This workspace now contains a starter build for a law firm website using `Python + Django + Wagtail + SQLite`.

## Recommended stack

- Backend and CMS: `Django` + `Wagtail`
- Database: `SQLite` for launch
- Frontend: Django templates, custom CSS, vanilla JavaScript
- Hosting: `AWS Lightsail` for the app, `GoDaddy` DNS for the domain
- Newsletter publishing: Wagtail pages for archive, optional `Brevo` or `Amazon SES` later for email sending

## Why this stack

- Lowest complexity for your current skills: Python and SQLite are enough here.
- Low monthly cost: a single small Lightsail instance is usually the most predictable low-cost path.
- Easy for a non-technical lawyer to update: Wagtail gives a proper admin panel instead of asking him to edit code or Git content.
- Modern-looking site without Angular overhead: this kind of law firm website is content-driven, not app-driven.

## Project structure

- `ajmani_site/`: Django and Wagtail project
- `ajmani_site/home/`: homepage, inner pages, contact page, and blog models
- `ajmani_site/insights/`: newsletter archive and newsletter issue pages, including optional PDF uploads
- `docs/`: setup and deployment notes

## Operations guide

- `docs/lalit-workflow.md`: how Lalit updates pages, publishes newsletters, receives enquiries, and how to enable email delivery plus dynamic Google reviews

## Local setup

From the workspace root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\ajmani_site\requirements.txt
cd .\ajmani_site\
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py seed_ajmani_content
..\.venv\Scripts\python.exe manage.py createsuperuser
..\.venv\Scripts\python.exe manage.py runserver
```

Open:

- Site: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

If port `8000` is busy on your machine, run:

```powershell
..\.venv\Scripts\python.exe manage.py runserver 8011
```

Then open:

- Site: `http://127.0.0.1:8011/`
- Admin: `http://127.0.0.1:8011/admin/`

## Open in VS Code

- Open `ajmani-and-law-partners.code-workspace` in VS Code.
- Use the bundled tasks in `.vscode/tasks.json` for install, migrate, seed, and runserver.
- Use the `Django: runserver` launch profile if you want to start the app from the VS Code debugger.

## Website disclaimer

- A first-visit disclaimer popup is now built into the shared site layout.
- Visitors can accept it once, and it can be reopened from the footer.

## What to edit in admin

- Update the homepage with the actual lawyer bio, office details, and Google review configuration.
- Edit the inner pages under `About Us`, `Expertise`, `Blog`, and `Contact`.
- Add monthly newsletter pages inside `Newsletters`.
- Optionally attach a PDF file to each newsletter page so visitors can open the issue directly.
- Add blog posts inside `Blog`.
- Upload the firm logo, founder portrait, and any office or courtroom-safe imagery.

## Current page tree

- `Home`
- `About Us`
- `Expertise`
- `Blog`
- `Contact`
- `Newsletters`

## Current capabilities

- Multi-page top navigation with dropdown sections
- Homepage with Google reviews, WhatsApp widget, disclaimer popup, and enquiry form
- Newsletter subscriptions and newsletter-email workflow
- Separate blog section that can be delegated to junior editors in Wagtail
- Google Maps office embed and Google listing links
