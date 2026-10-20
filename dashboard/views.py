from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.db import transaction
from courses.models import Topic
from materials.models import Material
from quizzes.models import Attempt, Choice, Question, Quiz
from .forms import MaterialForm, QuizBuilderForm, TopicForm
from courses.templatetags.ui import translate_ui
admin_required = user_passes_test(lambda user: user.is_active and user.is_staff, login_url="login")
dashboard_access = user_passes_test(lambda user: user.is_active and user.is_staff and (user.is_superuser or user.has_perm("courses.view_topic") or user.has_perm("materials.view_material") or user.has_perm("quizzes.view_quiz") or user.has_perm("quizzes.add_quiz")), login_url="login")
@dashboard_access
def overview(request):
    can_view_results = request.user.is_superuser or request.user.has_perm("quizzes.view_attempt")
    attempts = Attempt.objects.select_related("user", "quiz")[:8] if can_view_results else []
    return render(request, "dashboard/overview.html", {"topic_count": Topic.objects.count(), "material_count": Material.objects.count(), "attempts": attempts, "drafts": Topic.objects.exclude(status="published")[:6]})
@admin_required
@permission_required("courses.view_topic", raise_exception=True)
def topic_manage(request): return render(request, "dashboard/topics.html", {"topics": Topic.objects.select_related("section")})
@admin_required
def topic_edit(request, pk=None):
    permission = "courses.change_topic" if pk else "courses.add_topic"
    if not request.user.is_superuser and not request.user.has_perm(permission):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    instance = get_object_or_404(Topic, pk=pk) if pk else None; form = TopicForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid(): form.save(); messages.success(request, translate_ui("topic_saved")); return redirect("dashboard-topics")
    return render(request, "dashboard/form.html", {"form": form, "title": "Новая тема" if not instance else "Редактирование темы"})
@admin_required
@permission_required("courses.delete_topic", raise_exception=True)
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == "POST": topic.delete(); messages.success(request, translate_ui("topic_deleted")); return redirect("dashboard-topics")
    return render(request, "dashboard/confirm_delete.html", {"object": topic})
@admin_required
@permission_required("materials.add_material", raise_exception=True)
def material_upload(request):
    form = MaterialForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid(): form.save(); messages.success(request, translate_ui("material_uploaded")); return redirect("dashboard-overview")
    return render(request, "dashboard/form.html", {"form": form, "title": "Загрузка материала", "upload": True})


def _builder_data(quiz=None, data=None):
    if data is not None:
        questions = []
        for question_index in range(int(data.get("question-count", 0) or 0)):
            choice_count = int(data.get(f"questions-{question_index}-choice-count", 0) or 0)
            questions.append({
                "text": data.get(f"questions-{question_index}-text", ""),
                "explanation": data.get(f"questions-{question_index}-explanation", ""),
                "correct": data.get(f"questions-{question_index}-correct", ""),
                "choices": [data.get(f"questions-{question_index}-choice-{choice_index}", "") for choice_index in range(choice_count)],
            })
        return questions
    if quiz:
        return [{"text": question.text, "explanation": question.explanation, "correct": str(next((index for index, choice in enumerate(question.choices.all()) if choice.is_correct), "")), "choices": [choice.text for choice in question.choices.all()]} for question in quiz.questions.prefetch_related("choices")]
    return [{"text": "", "explanation": "", "correct": "", "choices": ["", ""]}]


def _save_questions(quiz, data):
    questions = _builder_data(data=data)
    if not questions:
        raise ValueError("Добавьте хотя бы один вопрос.")
    prepared = []
    for number, question in enumerate(questions, start=1):
        text = question["text"].strip()
        choices = [choice.strip() for choice in question["choices"] if choice.strip()]
        try:
            correct_index = int(question["correct"])
        except (TypeError, ValueError):
            correct_index = -1
        if not text:
            raise ValueError(f"Заполните текст вопроса {number}.")
        if len(choices) < 2:
            raise ValueError(f"В вопросе {number} нужно минимум два варианта ответа.")
        original_choices = [choice.strip() for choice in question["choices"]]
        if correct_index < 0 or correct_index >= len(original_choices) or not original_choices[correct_index]:
            raise ValueError(f"Выберите один правильный ответ для вопроса {number}.")
        prepared.append((text, question["explanation"].strip(), choices, original_choices[correct_index]))
    quiz.questions.all().delete()
    for order, (text, explanation, choices, correct_choice) in enumerate(prepared, start=1):
        question = Question.objects.create(quiz=quiz, text=text, explanation=explanation, order=order, multiple=False)
        for choice_text in choices:
            Choice.objects.create(question=question, text=choice_text, is_correct=choice_text == correct_choice)


@admin_required
@permission_required("quizzes.view_quiz", raise_exception=True)
def quiz_manage(request):
    return render(request, "dashboard/quizzes.html", {"quizzes": Quiz.objects.select_related("topic").prefetch_related("questions")})


@admin_required
def quiz_edit(request, pk=None):
    quiz = get_object_or_404(Quiz, pk=pk) if pk else None
    permission = "quizzes.change_quiz" if quiz else "quizzes.add_quiz"
    required = (permission, "quizzes.add_question", "quizzes.add_choice")
    if not request.user.is_superuser and not all(request.user.has_perm(code) for code in required):
        raise PermissionDenied
    if quiz and quiz.attempts.exists():
        messages.error(request, "Нельзя изменить вопросы теста, который уже проходили пользователи.")
        return redirect("dashboard-quizzes")
    form = QuizBuilderForm(request.POST or None, instance=quiz)
    builder_data = _builder_data(quiz=quiz, data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                saved_quiz = form.save()
                _save_questions(saved_quiz, request.POST)
        except ValueError as error:
            form.add_error(None, str(error))
        else:
            messages.success(request, "Тест сохранён.")
            return redirect("dashboard-quizzes")
    return render(request, "dashboard/quiz_builder.html", {"form": form, "quiz": quiz, "builder_data": builder_data})
