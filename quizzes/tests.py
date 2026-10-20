from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Question, Quiz
class QuizTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("student", password="safe-pass-123")
        self.quiz = Quiz.objects.create(title="Основы", published=True)
        self.question = Question.objects.create(quiz=self.quiz, text="Что относится к логистике?")
        self.correct = Choice.objects.create(question=self.question, text="Планирование потоков", is_correct=True)
        self.wrong = Choice.objects.create(question=self.question, text="Случайный ответ")
    def test_score_is_calculated_server_side(self):
        self.client.force_login(self.user)
        start = self.client.post(reverse("quiz-start", args=[self.quiz.pk]))
        self.assertEqual(start.status_code, 302)
        response = self.client.post(start.url, {f"question_{self.question.pk}": self.correct.pk})
        self.assertRedirects(response, reverse("quiz-result", args=[1]))
        self.assertContains(self.client.get(response.url), "100%")
    def test_attempt_limit_blocks_new_attempt(self):
        self.quiz.max_attempts = 1; self.quiz.save(); self.client.force_login(self.user)
        start = self.client.post(reverse("quiz-start", args=[self.quiz.pk])); self.client.post(start.url, {f"question_{self.question.pk}": self.correct.pk})
        self.assertRedirects(self.client.post(reverse("quiz-start", args=[self.quiz.pk])), reverse("quiz-list"))


class AdminQuizBuilderTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser("admin", "admin@example.test", "safe-pass-123")
        self.student = User.objects.create_user("learner", password="safe-pass-123")

    def test_admin_can_build_a_published_quiz_with_questions_and_choices(self):
        self.client.force_login(self.admin_user)
        quiz_add = reverse("admin:quizzes_quiz_add")
        response = self.client.post(quiz_add, {
            "title": "Новый тест", "description": "Проверка знаний", "published": "on",
            "max_attempts": "0", "time_limit_minutes": "0",
            "questions-TOTAL_FORMS": "1", "questions-INITIAL_FORMS": "0",
            "questions-MIN_NUM_FORMS": "0", "questions-MAX_NUM_FORMS": "1000",
            "questions-0-text": "Выберите верный ответ", "questions-0-explanation": "Пояснение", "questions-0-order": "1",
        })
        self.assertEqual(response.status_code, 302)
        quiz = Quiz.objects.get(title="Новый тест")
        question = quiz.questions.get()

        response = self.client.post(reverse("admin:quizzes_question_change", args=[question.pk]), {
            "quiz": quiz.pk, "text": question.text, "explanation": question.explanation, "order": "1",
            "choices-TOTAL_FORMS": "4", "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "0", "choices-MAX_NUM_FORMS": "1000",
            "choices-0-text": "Верный вариант", "choices-0-is_correct": "on",
            "choices-1-text": "Неверный вариант",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(question.choices.count(), 2)
        self.assertTrue(question.choices.get(text="Верный вариант").is_correct)

        self.client.force_login(self.student)
        self.assertContains(self.client.get(reverse("quiz-list")), "Новый тест")
        start = self.client.post(reverse("quiz-start", args=[quiz.pk]))
        self.assertEqual(start.status_code, 302)
        self.assertContains(self.client.get(start.url), "Верный вариант")
