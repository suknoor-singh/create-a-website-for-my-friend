from datetime import date

from home.models import (
    BlogIndexPage,
    BlogPage,
    ContactInquiry,
    ContactPage,
    HomePage,
    NewsletterSubscriber,
    SectionIndexPage,
    StandardContentPage,
)
from insights.models import NewsletterIndexPage, NewsletterPage

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase


class HomeSetUpTests(WagtailPageTestCase):
    """
    Tests for basic page structure setup and HomePage creation.
    """

    def test_root_create(self):
        root_page = Page.objects.get(pk=1)
        self.assertIsNotNone(root_page)

    def test_homepage_create(self):
        root_page = Page.objects.get(pk=1)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        self.assertTrue(HomePage.objects.filter(title="Home").exists())


class HomeTests(WagtailPageTestCase):
    """
    Tests for homepage functionality and rendering.
    """

    def setUp(self):
        """
        Create a homepage instance for testing.
        """
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)
        self.about_index = SectionIndexPage(title="About Us", slug="about-us", show_in_menus=True)
        self.homepage.add_child(instance=self.about_index)
        self.about_page = StandardContentPage(
            title="Who We Are",
            slug="who-we-are",
            intro="Intro",
            body="<p>Body</p>",
            show_in_menus=True,
        )
        self.about_index.add_child(instance=self.about_page)
        self.blog_index = BlogIndexPage(title="Blog", slug="blog", show_in_menus=True)
        self.homepage.add_child(instance=self.blog_index)
        self.blog_page = BlogPage(
            title="Example Blog",
            slug="example-blog",
            publication_date=date(2026, 5, 1),
            summary="Summary",
            body="<p>Blog body</p>",
        )
        self.blog_index.add_child(instance=self.blog_page)
        self.contact_page = ContactPage(title="Contact", slug="contact", show_in_menus=True)
        self.homepage.add_child(instance=self.contact_page)
        self.newsletter_index = NewsletterIndexPage(title="Newsletters", slug="newsletters", show_in_menus=True)
        self.homepage.add_child(instance=self.newsletter_index)
        self.newsletter_page = NewsletterPage(
            title="May 2026 Newsletter",
            slug="may-2026-newsletter",
            publication_date=date(2026, 5, 31),
            summary="Monthly legal update",
            body="<p>Newsletter body</p>",
        )
        self.newsletter_index.add_child(instance=self.newsletter_page)

    def test_homepage_is_renderable(self):
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_section_index_page_is_renderable(self):
        self.assertPageIsRenderable(self.about_index)

    def test_standard_content_page_is_renderable(self):
        self.assertPageIsRenderable(self.about_page)

    def test_blog_pages_are_renderable(self):
        self.assertPageIsRenderable(self.blog_index)
        self.assertPageIsRenderable(self.blog_page)

    def test_contact_page_is_renderable(self):
        self.assertPageIsRenderable(self.contact_page)

    def test_newsletter_pages_are_renderable(self):
        self.assertPageIsRenderable(self.newsletter_index)
        self.assertPageIsRenderable(self.newsletter_page)

    def test_newsletter_subscription_view(self):
        response = self.client.post(
            "/newsletter/subscribe/",
            {"email": "subscriber@example.com"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewsletterSubscriber.objects.filter(email="subscriber@example.com").exists())

    def test_contact_inquiry_view(self):
        response = self.client.post(
            "/contact/submit/",
            {
                "name": "Prospective Client",
                "email": "client@example.com",
                "phone": "9999999999",
                "message": "I need help with a property dispute.",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactInquiry.objects.filter(email="client@example.com").exists())
