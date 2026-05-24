from datetime import date

from django.core.management.base import BaseCommand

from wagtail.models import Page, Site

from home.models import BlogIndexPage, BlogPage, ContactPage, HomePage, SectionIndexPage, StandardContentPage
from insights.models import NewsletterIndexPage


class Command(BaseCommand):
    help = "Populate the site with Ajmani and Law Partners starter content."

    def handle(self, *args, **options):
        def ensure_child(parent, model, slug, **defaults):
            instance = parent.get_children().type(model).filter(slug=slug).first()
            if instance:
                page = instance.specific
                for field, value in defaults.items():
                    setattr(page, field, value)
                page.save_revision().publish()
                return page

            page = model(slug=slug, **defaults)
            parent.add_child(instance=page)
            page.save_revision().publish()
            return page

        homepage = HomePage.objects.first()
        if homepage is None:
            root_page = Page.get_first_root_node()
            homepage = HomePage(title="Home", slug="home")
            root_page.add_child(instance=homepage)

        homepage.intro_kicker = "Advocate Lalit Ajmani"
        homepage.hero_title = "Litigation counsel for district courts, the Delhi High Court, and Supreme Court matters."
        homepage.hero_subtitle = (
            "Ajmani and Law Partners is a New Delhi litigation practice led by Lalit Ajmani, "
            "serving individuals and businesses with practical advice, courtroom readiness, and clear communication."
        )
        homepage.primary_cta_label = "Call now"
        homepage.primary_cta_link = "tel:+919654431469"
        homepage.secondary_cta_label = "Read newsletters"
        homepage.secondary_cta_link = "#newsletters"
        homepage.credibility_points = [
            {"type": "point", "value": "5.0 Google rating"},
            {"type": "point", "value": "68 Google reviews"},
            {"type": "point", "value": "Janakpuri, New Delhi office"},
            {"type": "point", "value": "Founder-led litigation practice"},
        ]
        homepage.firm_overview_title = "A Delhi litigation practice built around clarity, responsiveness, and courtroom focus"
        homepage.firm_overview = (
            "<p>Ajmani and Law Partners is a New Delhi-based law firm representing clients in litigation, "
            "advisory, and drafting matters. The practice is positioned for appearances in district courts, "
            "the Delhi High Court, and matters requiring Supreme Court briefing and representation.</p>"
            "<p>The firm combines hands-on matter ownership with a practical, client-facing approach so that "
            "people understand both the legal position and the next procedural step.</p>"
        )
        homepage.founder_name = "Lalit Ajmani"
        homepage.founder_designation = "Founding and Managing Partner"
        homepage.founder_linkedin_url = "https://in.linkedin.com/in/lalit-ajmani-0089a155"
        homepage.founder_bio = (
            "<p>Lalit Ajmani is the founding and managing partner of Ajmani and Law Partners. "
            "Publicly available profiles describe him as a litigation lawyer based in New Delhi, with experience across "
            "civil, commercial, defamation, matrimonial, and related dispute work.</p>"
            "<p>His published profile also reflects writing and commentary on legal developments, which aligns well "
            "with the firm's monthly newsletter strategy.</p>"
        )
        homepage.founder_highlights = [
            {"type": "highlight", "value": "Founder and managing partner of Ajmani and Law Partners"},
            {"type": "highlight", "value": "Based in New Delhi with a Janakpuri office"},
            {"type": "highlight", "value": "Publishes commentary and legal insights"},
            {"type": "highlight", "value": "Client-facing, litigation-focused practice"},
        ]
        homepage.court_coverage = [
            {
                "type": "court",
                "value": {
                    "name": "Delhi District Courts",
                    "detail": "Representation for trial-stage, procedural, and hearing-driven matters across district court forums.",
                },
            },
            {
                "type": "court",
                "value": {
                    "name": "Delhi High Court",
                    "detail": "Writ, appellate, and complex civil or commercial matters that require disciplined briefing and appearance work.",
                },
            },
            {
                "type": "court",
                "value": {
                    "name": "Supreme Court of India",
                    "detail": "Support for matters that require apex-court strategy, briefing, filings, and coordinated representation.",
                },
            },
        ]
        homepage.practice_areas = [
            {
                "type": "practice",
                "value": {
                    "title": "Civil Litigation",
                    "description": "Disputes involving property, recovery, contractual issues, injunctions, and other civil court matters.",
                },
            },
            {
                "type": "practice",
                "value": {
                    "title": "Commercial Disputes",
                    "description": "Commercial conflicts requiring practical legal strategy, drafting, and representation before appropriate forums.",
                },
            },
            {
                "type": "practice",
                "value": {
                    "title": "Defamation and Reputation Matters",
                    "description": "Advice and representation in matters where reputation, publications, or business standing are at stake.",
                },
            },
            {
                "type": "practice",
                "value": {
                    "title": "Matrimonial and Family Disputes",
                    "description": "Sensitive dispute handling with a focus on process clarity, court readiness, and timely communication.",
                },
            },
            {
                "type": "practice",
                "value": {
                    "title": "Cheque Bounce and Recovery",
                    "description": "Efficient handling of Section 138 and recovery-linked matters where speed and documentation matter.",
                },
            },
            {
                "type": "practice",
                "value": {
                    "title": "Advisory and Drafting",
                    "description": "Contractual, compliance, and strategic drafting support for clients who need clear legal documentation.",
                },
            },
        ]
        homepage.testimonials = [
            {
                "type": "testimonial",
                "value": {
                    "quote": "My case was settled through the Ajmani sir, and the services were quite satisfactory. Finally, my case was concluded in the Delhi High Court because of sir's efforts.",
                    "author": "Barkha Kardam",
                    "rating": 5,
                    "source": "Google Reviews",
                },
            },
            {
                "type": "testimonial",
                "value": {
                    "quote": "I had a great experience working with Advocate Lalit Ajmani. He's not just knowledgeable and professional, but also really approachable and easy to communicate with.",
                    "author": "Sarthak Mahajan",
                    "rating": 5,
                    "source": "Google Reviews",
                },
            },
            {
                "type": "testimonial",
                "value": {
                    "quote": "It has been a truly wonderful experience working with Advocate Lalit Ajmani Sir. He has been an incredible mentor who has greatly enriched my legal journey.",
                    "author": "Diptanshu Kukrety",
                    "rating": 5,
                    "source": "Google Reviews",
                },
            },
        ]
        homepage.newsletter_title = "Monthly legal newsletters"
        homepage.newsletter_intro = (
            "Use this section for concise updates on judgments, litigation trends, procedural changes, and practical legal commentary."
        )
        homepage.google_reviews_query = "Advocate Lalit Ajmani, Janakpuri, New Delhi"
        homepage.google_business_share_url = "https://share.google/uWgDGPjVvt7nrNqtQ"
        homepage.google_maps_url = "https://share.google/uWgDGPjVvt7nrNqtQ"
        homepage.google_maps_embed_query = "C4G-17A, C4G, Block C4H, Janakpuri, New Delhi, Delhi 110058"
        homepage.whatsapp_number = "919654431469"
        homepage.whatsapp_default_message = (
            "Hello, I would like to discuss a legal matter with Ajmani and Law Partners."
        )
        homepage.contact_phone = "+91 96544 31469"
        homepage.contact_email = "lalit@ajmaniandlawpartners.com"
        homepage.office_address = "C4G-17A, C4G, Block C4H,\nJanakpuri, New Delhi, Delhi 110058"
        homepage.compliance_note = (
            "As required by professional norms, this website is intended only for informational purposes and does not constitute solicitation or legal advice."
        )
        homepage.show_in_menus = False
        homepage.save_revision().publish()

        about_index = ensure_child(
            homepage,
            SectionIndexPage,
            "about-us",
            title="About Us",
            intro=(
                "Learn how Ajmani and Law Partners approaches client service, litigation strategy, and professional standards."
            ),
            body=(
                "<p>This section works like the reference-style inner page menu you shared. "
                "Each page can be edited independently from the Wagtail admin and expanded over time as the firm grows.</p>"
            ),
            show_in_menus=True,
        )

        about_pages = [
            (
                "who-we-are",
                "Who We Are",
                "A founder-led litigation practice serving clients across Delhi with practical advice and disciplined court representation.",
                "<p>Ajmani and Law Partners is built around hands-on matter ownership. Clients come to the firm for practical guidance, direct communication, and representation that stays grounded in procedure, timing, and real courtroom requirements.</p><p>The practice is suited to disputes, advisory work, drafting, and litigation support where clarity and responsiveness matter.</p>",
                ["Founder-led client relationships", "Delhi-focused litigation practice", "Clear procedural communication"],
            ),
            (
                "founder-and-leadership",
                "Founder and Leadership",
                "The firm's leadership remains closely involved in strategy, filings, appearances, and client communication.",
                "<p>Lalit Ajmani leads the practice with a litigation-first mindset and direct involvement in matter strategy. This helps maintain continuity between advice, filings, hearings, and client updates.</p><p>The leadership model is intentionally lean so that clients are not pushed through unnecessary layers before receiving actionable guidance.</p>",
                ["Direct founder involvement", "Lean decision-making", "Hands-on matter supervision"],
            ),
            (
                "courtroom-approach",
                "Courtroom Approach",
                "The firm prepares matters with equal attention to legal positioning, record-building, and hearing readiness.",
                "<p>Good litigation work is not only about argument. It is about building the record, keeping filings sharp, anticipating procedural turns, and presenting the matter cleanly before the court.</p><p>The firm's approach therefore combines drafting discipline with practical hearing preparation.</p>",
                ["Drafting discipline", "Hearing preparation", "Record-focused strategy"],
            ),
            (
                "client-service",
                "Client Service",
                "Clients should understand the status of a matter, the next procedural step, and the strategic choices available.",
                "<p>Ajmani and Law Partners emphasizes communication that is direct and useful. Instead of overwhelming clients with jargon, the goal is to explain where the matter stands, what comes next, and what decisions need to be taken.</p><p>This is especially important in disputes where timing, documentation, and expectations have to be managed carefully.</p>",
                ["Clear updates", "Practical explanations", "Responsive communication"],
            ),
            (
                "memberships-and-recognition",
                "Memberships and Recognition",
                "Use this page to highlight bar memberships, speaking engagements, publications, or external recognition as the firm grows.",
                "<p>This section is intentionally structured for future credibility additions. Over time, the firm can use it to highlight bar memberships, legal publications, event participation, or notable recognition.</p><p>Because it is a standalone page, your team can update it without affecting the rest of the website layout.</p>",
                ["Future-ready credibility page", "Suitable for publications and memberships", "Easy to update over time"],
            ),
        ]

        for slug, title, intro, body, highlights in about_pages:
            ensure_child(
                about_index,
                StandardContentPage,
                slug,
                title=title,
                intro=intro,
                body=body,
                highlights=[{"type": "highlight", "value": item} for item in highlights],
                show_in_menus=True,
            )

        expertise_index = ensure_child(
            homepage,
            SectionIndexPage,
            "expertise",
            title="Expertise",
            intro="Focused service pages for the kinds of matters clients are most likely to search for before getting in touch.",
            body=(
                "<p>These pages are structured as dedicated service pages rather than a single long list. "
                "That makes the website easier to navigate and gives the firm room to expand each practice area with more detail later.</p>"
            ),
            show_in_menus=True,
        )

        expertise_pages = [
            (
                "civil-litigation",
                "Civil Litigation",
                "Representation in injunction, recovery, contractual, and other civil disputes where procedural strategy matters from day one.",
            ),
            (
                "commercial-disputes",
                "Commercial Disputes",
                "Support for business conflicts requiring practical legal analysis, pleadings, and coordinated courtroom strategy.",
            ),
            (
                "defamation-and-reputation",
                "Defamation and Reputation Matters",
                "Advice and representation where publications, allegations, or online content affect personal or business reputation.",
            ),
            (
                "matrimonial-and-family",
                "Matrimonial and Family Disputes",
                "Sensitive handling of family-related disputes with attention to procedure, pace, and clear communication.",
            ),
            (
                "cheque-bounce-and-recovery",
                "Cheque Bounce and Recovery",
                "Section 138 NI Act and recovery-linked matters that require documentation discipline and efficient follow-through.",
            ),
            (
                "advisory-and-drafting",
                "Advisory and Drafting",
                "Contracts, notices, replies, and practical drafting support for clients who need legal clarity before disputes escalate.",
            ),
        ]

        for slug, title, intro in expertise_pages:
            ensure_child(
                expertise_index,
                StandardContentPage,
                slug,
                title=title,
                intro=intro,
                body=(
                    f"<p>{intro}</p>"
                    "<p>This page is intentionally editable from the Wagtail admin so the firm can later add "
                    "more specific examples, FAQs, process notes, or sector detail without redesigning the whole site.</p>"
                ),
                highlights=[
                    {"type": "highlight", "value": "Useful as a dedicated service landing page"},
                    {"type": "highlight", "value": "Can be expanded with FAQs and process notes"},
                    {"type": "highlight", "value": "Suitable for future SEO improvement"},
                ],
                show_in_menus=True,
            )

        blog_index = ensure_child(
            homepage,
            BlogIndexPage,
            "blog",
            title="Blog",
            intro=(
                "Short legal explainers, practical updates, and article-style commentary that junior team members can help maintain."
            ),
            show_in_menus=True,
        )

        ensure_child(
            blog_index,
            BlogPage,
            "understanding-court-readiness",
            title="Understanding court-readiness before the first hearing",
            publication_date=date(2026, 5, 1),
            summary="A short example article showing how the blog can be used for client-friendly legal writing.",
            author_name="Editorial Team",
            body=(
                "<p>Clients often think litigation starts in court. In practice, much of the important work begins earlier: "
                "documents need to be organized, timelines need to be checked, and the factual record has to be prepared carefully.</p>"
                "<p>A good first hearing depends not only on legal arguments, but on procedural readiness. "
                "That is why early advice, document review, and realistic planning can materially improve how a matter moves forward.</p>"
            ),
            show_in_menus=False,
        )

        ensure_child(
            homepage,
            ContactPage,
            "contact",
            title="Contact",
            intro="Share your matter briefly and the firm can respond by phone, email, or WhatsApp.",
            body=(
                "<p>Use this page for new enquiries, follow-up discussions, or scheduling a first conversation with the firm.</p>"
            ),
            show_in_menus=True,
        )

        newsletter_index = NewsletterIndexPage.objects.child_of(homepage).first()
        if newsletter_index is None:
            newsletter_index = NewsletterIndexPage(
                title="Newsletters",
                slug="newsletters",
                intro=(
                    "A running archive for monthly legal updates from Ajmani and Law Partners. "
                    "Publish a new issue each month from the admin panel or upload a PDF-backed issue for visitors to open directly."
                ),
            )
            homepage.add_child(instance=newsletter_index)
        else:
            newsletter_index.title = "Newsletters"
            newsletter_index.slug = "newsletters"
            newsletter_index.intro = (
                "A running archive for monthly legal updates from Ajmani and Law Partners. "
                "Publish a new issue each month from the admin panel or upload a PDF-backed issue for visitors to open directly."
            )
        newsletter_index.show_in_menus = True
        newsletter_index.save_revision().publish()

        Site.objects.update_or_create(
            hostname="localhost",
            defaults={
                "root_page": homepage,
                "site_name": "Ajmani and Law Partners",
                "is_default_site": True,
                "port": 8000,
            },
        )
        Site.objects.update_or_create(
            hostname="localhost",
            defaults={
                "root_page": homepage,
                "site_name": "Ajmani and Law Partners",
                "is_default_site": False,
                "port": 8011,
            },
        )
        Site.objects.update_or_create(
            hostname="127.0.0.1",
            defaults={
                "root_page": homepage,
                "site_name": "Ajmani and Law Partners",
                "is_default_site": False,
                "port": 8000,
            },
        )
        Site.objects.update_or_create(
            hostname="127.0.0.1",
            defaults={
                "root_page": homepage,
                "site_name": "Ajmani and Law Partners",
                "is_default_site": False,
                "port": 8011,
            },
        )

        self.stdout.write(self.style.SUCCESS("Ajmani and Law Partners content seeded successfully."))
