from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Topic, TopicProgress
class CourseAccessTests(TestCase):
    def setUp(self): self.topic = Topic.objects.create(title="Цепочка поставок", slug="supply-chain", summary="Описание", status="published")
    def test_public_topic_is_visible(self): self.assertContains(self.client.get(reverse("topic-detail", args=[self.topic.slug])), "Logistika tizimi va ta’minot zanjiri")
    def test_home_page_is_available(self): self.assertContains(self.client.get(reverse("home")), "LogiLearn")
    def test_uzbek_is_default_interface_language(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Bosh sahifa")
        self.assertEqual(response.wsgi_request.LANGUAGE_CODE, "uz")
    def test_selected_language_is_kept_in_cookie(self):
        response = self.client.post(reverse("set_language"), {"language": "en", "next": reverse("home")})
        self.assertEqual(response.status_code, 302)
        self.client.cookies["logilearn_language"] = response.cookies["logilearn_language"].value
        self.assertContains(self.client.get(reverse("home")), "Home")
    def test_builtin_topic_card_is_translated_without_changing_database_value(self):
        self.client.post("/i18n/setlang/", {"language": "uz", "next": reverse("home")})
        uzbek = self.client.get(reverse("home"))
        self.assertContains(uzbek, "Logistika tizimi va ta’minot zanjiri")
        self.client.post("/i18n/setlang/", {"language": "en", "next": reverse("home")})
        english = self.client.get(reverse("home"))
        self.assertContains(english, "Logistics System and Supply Chain")
        self.assertEqual(Topic.objects.get(pk=self.topic.pk).title, "Цепочка поставок")
    def test_all_languages_render_server_translated_interface_across_sections(self):
        cases = [("uz", "/materials/", "O‘quv materiallari"), ("ru", "/tests/", "Контроль знаний"), ("en", "/glossary/", "Brief definitions")]
        for language, path, expected in cases:
            self.client.post("/i18n/setlang/", {"language": language, "next": path})
            response = self.client.get(path)
            self.assertEqual(response.wsgi_request.LANGUAGE_CODE, language)
            self.assertContains(response, expected)
    def test_progress_requires_login(self): self.assertEqual(self.client.post(reverse("toggle-complete", args=[self.topic.slug])).status_code, 302)
    def test_progress_is_saved_for_authenticated_user(self):
        user = User.objects.create_user("learner", password="safe-pass-123")
        self.client.force_login(user); self.client.post(reverse("toggle-complete", args=[self.topic.slug]))
        self.assertTrue(TopicProgress.objects.filter(user=user, topic=self.topic).exists())
