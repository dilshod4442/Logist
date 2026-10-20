from django import forms
from django.utils.translation import get_language
from courses.models import Topic
from materials.models import Material
from quizzes.models import Quiz
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic; fields = ["section", "title", "slug", "summary", "objectives", "theory", "self_check", "status", "order"]
        widgets = {"summary": forms.Textarea(attrs={"rows": 3}), "objectives": forms.Textarea(attrs={"rows": 4}), "theory": forms.Textarea(attrs={"rows": 10}), "self_check": forms.Textarea(attrs={"rows": 4})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        language = (get_language() or "uz").split("-")[0]
        labels = {
            "uz": {"section":"Bo‘lim", "title":"Sarlavha", "slug":"URL nomi", "summary":"Qisqa tavsif", "objectives":"Ta’lim maqsadlari", "theory":"Nazariy material", "self_check":"O‘zini tekshirish savollari", "status":"Holat", "order":"Tartib"},
            "ru": {"section":"Раздел", "title":"Название", "slug":"URL-имя", "summary":"Краткое описание", "objectives":"Цели обучения", "theory":"Теоретический материал", "self_check":"Вопросы для самопроверки", "status":"Статус", "order":"Порядок"},
            "en": {"section":"Section", "title":"Title", "slug":"URL slug", "summary":"Short description", "objectives":"Learning objectives", "theory":"Theory material", "self_check":"Self-check questions", "status":"Status", "order":"Order"},
        }
        self._translate_labels(labels.get(language, labels["uz"]))
    def _translate_labels(self, labels):
        for name, label in labels.items():
            if name in self.fields: self.fields[name].label = label
        language = (get_language() or "uz").split("-")[0]
        statuses = {"uz": [("draft","Qoralama"),("published","Chop etilgan"),("hidden","Yashirilgan")], "ru": [("draft","Черновик"),("published","Опубликовано"),("hidden","Скрыто")], "en": [("draft","Draft"),("published","Published"),("hidden","Hidden")]}
        if "status" in self.fields: self.fields["status"].choices = statuses.get(language, statuses["uz"])
class MaterialForm(forms.ModelForm):
    class Meta: model = Material; fields = ["topic", "title", "description", "file", "is_public", "status"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        language = (get_language() or "uz").split("-")[0]
        labels = {
            "uz": {"topic":"Mavzu", "title":"Sarlavha", "description":"Tavsif", "file":"Fayl", "is_public":"Ommaviy material", "status":"Holat"},
            "ru": {"topic":"Тема", "title":"Название", "description":"Описание", "file":"Файл", "is_public":"Публичный материал", "status":"Статус"},
            "en": {"topic":"Topic", "title":"Title", "description":"Description", "file":"File", "is_public":"Public material", "status":"Status"},
        }
        for name, label in labels.get(language, labels["uz"]).items(): self.fields[name].label = label


class QuizBuilderForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["topic", "title", "description", "published", "max_attempts", "time_limit_minutes", "random_order"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
