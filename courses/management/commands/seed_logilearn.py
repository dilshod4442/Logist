from django.core.management.base import BaseCommand
from courses.models import Lecture, PracticeTask, Section, Topic
from glossary.models import Term
from quizzes.models import Choice, Question, Quiz
class Command(BaseCommand):
    help = "Добавляет стартовое демонстрационное содержание LogiLearn."
    def handle(self, *args, **options):
        section, _ = Section.objects.get_or_create(title="Основы логистики", defaults={"description":"Ключевые элементы системы", "order":1})
        records = [
            ("Логистическая система и цепочка поставок", "supply-chain", "Связь поставщиков, операций и потребителей в едином потоке.", "Определять участников цепочки поставок и описывать движение материального, информационного и финансового потоков."),
            ("Логистические процессы и их взаимосвязь", "logistics-processes", "Планирование, закупка, транспортировка, складирование и распределение.", "Понимать взаимозависимость процессов и находить точки передачи ответственности."),
            ("Анализ транспортной цепочки", "transport-chain", "Оценка маршрута, сроков, рисков и стоимости транспортировки.", "Сравнивать варианты перевозки по сроку, стоимости и риску."),
            ("Склад, запасы и распределение", "warehouse-inventory", "Планирование складских операций и уровня запасов.", "Выбирать показатели для контроля запасов и операций склада."),
            ("Управление операциями и KPI", "operations-kpi", "Мониторинг выполнения логистических операций по измеримым показателям.", "Рассчитывать и интерпретировать базовые показатели работы процесса."),
            ("Оптимизация и эффективность", "optimization-efficiency", "Поиск улучшений в затратах, ресурсах и уровне сервиса.", "Обосновывать меры оптимизации на основе данных."),
        ]
        topics = []
        for order, (title, slug, summary, objectives) in enumerate(records, 1):
            topic, _ = Topic.objects.update_or_create(slug=slug, defaults={"section": section, "title": title, "summary": summary, "objectives": objectives, "theory":"Дополнительный учебный материал. Логистическая задача рассматривается как управление взаимосвязанными потоками. Для обоснованного решения определите участников процесса, границы операции, измеряемый результат и ограничения.", "self_check":"Какие участники входят в процесс?\nКакие показатели подтвердят результат?\nКакие риски следует учесть?", "status":"published", "order":order})
            topics.append(topic)
            Lecture.objects.get_or_create(topic=topic, title=f"Введение: {title}", defaults={"body":"Дополнительный материал для самостоятельного чтения. Используйте тему как опорную структуру для анализа реальной операции.", "published":True})
            PracticeTask.objects.get_or_create(topic=topic, title="Кейс для анализа", defaults={"task":"Выберите знакомую поставку или операцию. Опишите участников, этапы, риски, показатели срока и стоимости.", "guidance":"Начните со схемы «поставщик — операция — получатель».", "published":True})
        for term, definition in [("Логистика", "Управление потоками ресурсов и связанной информацией от источника к потребителю."), ("Цепочка поставок", "Сеть организаций и процессов, обеспечивающих создание и доставку продукта."), ("KPI", "Измеримый показатель, который используют для оценки достижения цели."), ("Запас", "Ресурс, хранимый для обеспечения спроса или непрерывности операций."), ("Распределение", "Организация движения готовой продукции к потребителю.")]: Term.objects.get_or_create(term=term, defaults={"definition":definition})
        quiz, _ = Quiz.objects.get_or_create(title="Самопроверка: основы логистики", defaults={"topic":topics[0], "description":"Короткий тест по базовым понятиям.", "published":True, "random_order":True})
        question, _ = Question.objects.get_or_create(quiz=quiz, text="Что объединяет цепочка поставок?", defaults={"explanation":"Цепочка поставок связывает организации и процессы, обеспечивающие движение ценности."})
        Choice.objects.get_or_create(question=question, text="Поставщиков, операции и получателей", defaults={"is_correct":True})
        Choice.objects.get_or_create(question=question, text="Только складские помещения", defaults={"is_correct":False})
        self.stdout.write(self.style.SUCCESS("Стартовое содержание добавлено."))
