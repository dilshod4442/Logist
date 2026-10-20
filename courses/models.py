from django.conf import settings
from django.db import models
from django.urls import reverse

class PublishedQuerySet(models.QuerySet):
    def published(self): return self.filter(status="published")
class Section(models.Model):
    title = models.CharField("раздел", max_length=160)
    description = models.TextField("описание", blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    class Meta: ordering = ["order", "title"]
    def __str__(self): return self.title
class Topic(models.Model):
    STATUS = [("draft", "Черновик"), ("published", "Опубликовано"), ("hidden", "Скрыто")]
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True, related_name="topics")
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, max_length=240)
    summary = models.TextField("краткое описание")
    objectives = models.TextField("цели обучения", blank=True)
    theory = models.TextField("теоретический материал", blank=True)
    self_check = models.TextField("вопросы для самопроверки", blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="draft", db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PublishedQuerySet.as_manager()
    class Meta: ordering = ["order", "title"]
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse("topic-detail", kwargs={"slug": self.slug})
class Lecture(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="lectures")
    title = models.CharField(max_length=220); body = models.TextField(); order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, db_index=True)
    class Meta: ordering = ["order", "title"]
    def __str__(self): return self.title
class PracticeTask(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="practice_tasks")
    title = models.CharField(max_length=220); task = models.TextField(); guidance = models.TextField(blank=True)
    published = models.BooleanField(default=False, db_index=True)
    def __str__(self): return self.title
class TopicProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="topic_progress")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="progress_records")
    completed_at = models.DateTimeField(auto_now=True)
    class Meta: constraints = [models.UniqueConstraint(fields=["user", "topic"], name="unique_topic_progress")]
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="LogiLearn")
    tagline = models.CharField(max_length=220, default="Образовательный ресурс по логистике")
    logo = models.ImageField(upload_to="branding/", blank=True)
    class Meta: verbose_name = "настройка сайта"; verbose_name_plural = "настройки сайта"
    def __str__(self): return self.site_name
