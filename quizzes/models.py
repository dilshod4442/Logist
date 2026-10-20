from django.conf import settings
from django.db import models
from courses.models import Topic
class Quiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="quizzes")
    title = models.CharField(max_length=220); description = models.TextField(blank=True); published = models.BooleanField(default=False, db_index=True)
    max_attempts = models.PositiveIntegerField(default=0, help_text="0 — без ограничений")
    time_limit_minutes = models.PositiveIntegerField(default=0, help_text="0 — без ограничения"); random_order = models.BooleanField(default=False)
    def __str__(self): return self.title
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(); multiple = models.BooleanField(default=False, verbose_name="несколько правильных ответов")
    explanation = models.TextField(blank=True); order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["order", "id"]
    def __str__(self): return self.text[:80]
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=500); is_correct = models.BooleanField(default=False)
    def __str__(self): return self.text
class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    started_at = models.DateTimeField(auto_now_add=True); completed_at = models.DateTimeField(blank=True, null=True)
    score = models.PositiveIntegerField(default=0); total = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["-started_at"]
    @property
    def percentage(self): return round(self.score / self.total * 100) if self.total else 0
class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE); selected = models.ManyToManyField(Choice, blank=True); correct = models.BooleanField(default=False)
    class Meta: constraints = [models.UniqueConstraint(fields=["attempt", "question"], name="one_answer_each_question")]
