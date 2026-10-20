from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from .models import Answer, Attempt, Choice, Question, Quiz


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ("text", "is_correct")
    verbose_name = "вариант ответа"
    verbose_name_plural = "варианты ответов"


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ("text", "multiple", "explanation", "order")
    show_change_link = True
    verbose_name = "вопрос"
    verbose_name_plural = "вопросы"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("short_text", "quiz", "multiple", "order", "answer_count")
    list_filter = ("multiple", "quiz")
    search_fields = ("text", "quiz__title")
    list_editable = ("multiple", "order")
    fields = ("quiz", "text", "multiple", "explanation", "order")
    save_on_top = True

    @admin.display(description="вопрос")
    def short_text(self, obj):
        return obj.text[:90]

    @admin.display(description="вариантов")
    def answer_count(self, obj):
        return obj.choices.count()


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = (
        "title", "topic", "published", "question_count",
        "max_attempts", "time_limit_minutes", "random_order", "edit_questions",
    )
    list_filter = ("published", "topic")
    list_editable = ("published", "max_attempts", "time_limit_minutes")
    search_fields = ("title", "description")
    autocomplete_fields = ("topic",)
    fields = ("topic", "title", "description", "published", "max_attempts", "time_limit_minutes", "random_order")
    save_on_top = True

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_question_count=Count("questions"))

    @admin.display(description="вопросов", ordering="_question_count")
    def question_count(self, obj):
        return obj._question_count

    @admin.display(description="вопросы и ответы")
    def edit_questions(self, obj):
        url = reverse("admin:quizzes_question_changelist") + f"?quiz__id__exact={obj.pk}"
        return format_html('<a class="button" href="{}">Вопросы и ответы</a>', url)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "total", "percentage_display", "started_at", "completed_at")
    list_filter = ("quiz", "completed_at")
    search_fields = ("user__username", "quiz__title")
    readonly_fields = ("user", "quiz", "started_at", "completed_at", "score", "total")
    ordering = ("-started_at",)

    @admin.display(description="%")
    def percentage_display(self, obj):
        return f"{obj.percentage}%"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct", "question__quiz")
    list_editable = ("is_correct",)
    search_fields = ("text", "question__text")


admin.site.register(Answer)
