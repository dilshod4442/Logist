import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Answer, Attempt, Quiz
from courses.templatetags.ui import translate_ui
def quiz_list(request): return render(request, "quizzes/list.html", {"quizzes": Quiz.objects.filter(Q(topic__status="published") | Q(topic__isnull=True), published=True).select_related("topic")})
@login_required
def start(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, published=True)
    if quiz.max_attempts and Attempt.objects.filter(user=request.user, quiz=quiz, completed_at__isnull=False).count() >= quiz.max_attempts:
        messages.error(request, translate_ui("attempt_limit")); return redirect("quiz-list")
    attempt = Attempt.objects.create(user=request.user, quiz=quiz)
    ids = list(quiz.questions.values_list("id", flat=True))
    if quiz.random_order: random.shuffle(ids); request.session[f"quiz_order_{attempt.pk}"] = ids
    return redirect("quiz-take", pk=attempt.pk)
@login_required
def take(request, pk):
    attempt = get_object_or_404(Attempt.objects.select_related("quiz"), pk=pk, user=request.user)
    if attempt.completed_at: return redirect("quiz-result", pk=attempt.pk)
    if request.method == "POST": return submit(request, attempt)
    questions = list(attempt.quiz.questions.prefetch_related("choices"))
    ordered_ids = request.session.get(f"quiz_order_{attempt.pk}")
    if ordered_ids: questions.sort(key=lambda q: ordered_ids.index(q.id))
    return render(request, "quizzes/take.html", {"attempt": attempt, "questions": questions})
@login_required
@transaction.atomic
def submit(request, attempt):
    quiz = attempt.quiz
    timed_out = quiz.time_limit_minutes and (timezone.now() - attempt.started_at).total_seconds() > quiz.time_limit_minutes * 60
    if timed_out: messages.error(request, translate_ui("time_expired"))
    score = 0; questions = quiz.questions.prefetch_related("choices")
    for question in questions:
        selected_ids = [int(value) for value in request.POST.getlist(f"question_{question.pk}") if value.isdigit()]
        valid_ids = set(question.choices.values_list("id", flat=True)); selected_ids = set(selected_ids) & valid_ids
        correct_ids = set(question.choices.filter(is_correct=True).values_list("id", flat=True))
        answer = Answer.objects.create(attempt=attempt, question=question, correct=selected_ids == correct_ids)
        answer.selected.set(selected_ids)
        score += int(answer.correct and not timed_out)
    attempt.score, attempt.total, attempt.completed_at = score, questions.count(), timezone.now(); attempt.save()
    return redirect("quiz-result", pk=attempt.pk)
@login_required
def result(request, pk):
    attempt = get_object_or_404(Attempt.objects.select_related("quiz").prefetch_related("answers__question__choices", "answers__selected"), pk=pk, user=request.user, completed_at__isnull=False)
    return render(request, "quizzes/result.html", {"attempt": attempt})
