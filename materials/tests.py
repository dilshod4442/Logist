from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Material, validate_upload
class UploadTests(TestCase):
    def test_blocks_disallowed_extension(self):
        with self.assertRaises(ValidationError): validate_upload(SimpleUploadedFile("script.exe", b"data"))
    def test_allows_pdf(self): validate_upload(SimpleUploadedFile("guide.pdf", b"%PDF-1.7"))
    def test_rejects_extension_with_wrong_content_signature(self):
        with self.assertRaises(ValidationError): validate_upload(SimpleUploadedFile("fake.pdf", b"not a PDF"))

@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class MediaDeliveryTests(TestCase):
    def setUp(self):
        self.video = Material.objects.create(title="Sample video", file=SimpleUploadedFile("sample.mp4", b"0123456789"), status="published", is_public=True)
    def tearDown(self):
        if hasattr(self, "video") and self.video.file:
            self.video.file.delete(save=False)
    def test_video_stream_supports_http_ranges_and_inline_media_type(self):
        response = self.client.get(reverse("material-video-stream", args=[self.video.pk]), HTTP_RANGE="bytes=2-5")
        self.assertEqual(response.status_code, 206)
        self.assertEqual(response["Content-Range"], "bytes 2-5/10")
        self.assertEqual(response["Content-Type"], "video/mp4")
        self.assertEqual(b"".join(response.streaming_content), b"2345")
    def test_material_page_renders_video_player_not_file_download_card(self):
        response = self.client.get(reverse("material-list"))
        self.assertContains(response, "<video", html=False)
        self.assertContains(response, reverse("material-video-stream", args=[self.video.pk]))
