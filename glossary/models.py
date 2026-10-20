from django.db import models
class Term(models.Model):
    term = models.CharField(max_length=120, unique=True, db_index=True)
    definition = models.TextField(); letter = models.CharField(max_length=1, editable=False, db_index=True)
    published = models.BooleanField(default=True, db_index=True)
    class Meta: ordering = ["term"]
    def save(self, *args, **kwargs): self.letter = self.term[:1].upper(); super().save(*args, **kwargs)
    def __str__(self): return self.term
