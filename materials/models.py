import os, uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from courses.models import Topic
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "csv", "jpg", "jpeg", "png", "webp", "zip", "mp4", "webm"}
VIDEO_EXTENSIONS = {"mp4", "webm"}
def safe_upload_path(instance, filename): return f"materials/{uuid.uuid4().hex}{os.path.splitext(filename)[1].lower()}"
def validate_upload(file):
    ext = os.path.splitext(file.name)[1].lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS: raise ValidationError("Этот тип файла не разрешён.")
    if file.size > settings.MAX_UPLOAD_SIZE: raise ValidationError(f"Файл превышает лимит {settings.MAX_UPLOAD_SIZE // 1024 // 1024} МБ.")
    signatures = {
        "pdf": lambda head: head.startswith(b"%PDF-"),
        "jpg": lambda head: head.startswith(b"\xff\xd8\xff"), "jpeg": lambda head: head.startswith(b"\xff\xd8\xff"),
        "png": lambda head: head.startswith(b"\x89PNG\r\n\x1a\n"), "webp": lambda head: len(head) >= 12 and head[:4] == b"RIFF" and head[8:12] == b"WEBP",
        "zip": lambda head: head.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")),
        "doc": lambda head: head.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"), "xls": lambda head: head.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"), "ppt": lambda head: head.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"),
        "docx": lambda head: head.startswith(b"PK\x03\x04"), "xlsx": lambda head: head.startswith(b"PK\x03\x04"), "pptx": lambda head: head.startswith(b"PK\x03\x04"),
        "mp4": lambda head: len(head) >= 8 and head[4:8] == b"ftyp", "webm": lambda head: head.startswith(b"\x1aE\xdf\xa3"),
    }
    checker = signatures.get(ext)
    if checker:
        try:
            position = file.tell()
            file.seek(0)
            header = file.read(16)
            file.seek(position)
        except (AttributeError, OSError):
            raise ValidationError("Не удалось проверить тип файла.")
        if not checker(header):
            raise ValidationError("Содержимое файла не соответствует его расширению.")
def validate_video_upload(file):
    validate_upload(file)
    ext = os.path.splitext(file.name)[1].lower().lstrip(".")
    if ext not in VIDEO_EXTENSIONS:
        raise ValidationError("Для воспроизведения используйте MP4 (H.264) или WebM.")
class Material(models.Model):
    STATUS = [("draft", "Черновик"), ("published", "Опубликовано"), ("hidden", "Скрыто")]
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="materials")
    title = models.CharField(max_length=220); description = models.TextField(blank=True)
    file = models.FileField(upload_to=safe_upload_path, validators=[validate_upload])
    is_public = models.BooleanField(default=True); status = models.CharField(max_length=12, choices=STATUS, default="draft", db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
    @property
    def extension(self): return os.path.splitext(self.file.name)[1].upper().lstrip(".")
    @property
    def size(self): return self.file.size if self.file else 0
class Video(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="videos")
    title = models.CharField(max_length=220); description = models.TextField(blank=True)
    external_url = models.URLField(blank=True); video_file = models.FileField(upload_to=safe_upload_path, blank=True, validators=[validate_video_upload])
    cover = models.ImageField(upload_to="covers/", blank=True); status = models.CharField(max_length=12, choices=Material.STATUS, default="draft", db_index=True)
    def clean(self):
        if not self.external_url and not self.video_file: raise ValidationError("Добавьте файл видео или внешнюю ссылку.")
    def __str__(self): return self.title
