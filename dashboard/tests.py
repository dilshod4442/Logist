from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from courses.models import Topic
class DashboardAccessTests(TestCase):
    def test_regular_user_cannot_open_dashboard(self):
        user = User.objects.create_user("learner", password="safe-pass-123")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard-overview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
    def test_staff_can_create_topic_through_dashboard(self):
        user = User.objects.create_superuser("editor", password="safe-pass-123")
        self.client.force_login(user)
        response = self.client.post(reverse("dashboard-topic-new"), {"title":"Новая тема", "slug":"new-topic", "summary":"Описание", "status":"draft", "order":1})
        self.assertRedirects(response, reverse("dashboard-topics"))
        self.assertTrue(Topic.objects.filter(slug="new-topic").exists())
    def test_staff_without_permissions_cannot_view_topic_management(self):
        user = User.objects.create_user("staff", password="safe-pass-123", is_staff=True)
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("dashboard-topics")).status_code, 403)
        self.assertNotContains(self.client.get(reverse("home")), "Boshqaruv")
    def test_staff_with_permissions_can_manage_topics_and_uploads(self):
        user = User.objects.create_user("content-editor", password="safe-pass-123", is_staff=True)
        user.user_permissions.add(
            Permission.objects.get(codename="view_topic"), Permission.objects.get(codename="add_topic"),
            Permission.objects.get(codename="view_material"), Permission.objects.get(codename="add_material"),
        )
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("dashboard-topics")).status_code, 200)
        self.assertEqual(self.client.get(reverse("dashboard-material-upload")).status_code, 200)
        self.assertContains(self.client.get(reverse("home")), "Boshqaruv")
