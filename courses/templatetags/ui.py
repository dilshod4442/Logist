from django import template
from django.utils.translation import get_language

register = template.Library()

TEXT = {
    "skip_to_content": {"uz": "Tarkibga o‘tish", "ru": "К содержанию", "en": "Skip to content"},
    "open_menu": {"uz": "Menyuni ochish", "ru": "Открыть меню", "en": "Open menu"},
    "main_navigation": {"uz": "Asosiy navigatsiya", "ru": "Основная навигация", "en": "Main navigation"},
    "home": {"uz": "Bosh sahifa", "ru": "Главная", "en": "Home"},
    "topics": {"uz": "Mavzular", "ru": "Темы", "en": "Topics"},
    "lectures": {"uz": "Ma’ruzalar", "ru": "Лекции", "en": "Lectures"},
    "practice": {"uz": "Amaliyot", "ru": "Практика", "en": "Practice"},
    "materials": {"uz": "Materiallar", "ru": "Материалы", "en": "Materials"},
    "tests": {"uz": "Testlar", "ru": "Тесты", "en": "Tests"},
    "test": {"uz": "Test", "ru": "Тест", "en": "Test"},
    "glossary": {"uz": "Lug‘at", "ru": "Глоссарий", "en": "Glossary"},
    "dashboard": {"uz": "Boshqaruv", "ru": "Панель", "en": "Dashboard"},
    "sign_in": {"uz": "Kirish", "ru": "Войти", "en": "Sign in"},
    "sign_out": {"uz": "Chiqish", "ru": "Выйти", "en": "Sign out"},
    "language": {"uz": "Til", "ru": "Язык", "en": "Language"},
    "theme": {"uz": "Mavzu", "ru": "Тема", "en": "Theme"},
    "switch_theme": {"uz": "Rangli mavzuni almashtirish", "ru": "Переключить цветовую тему", "en": "Switch colour theme"},
    "site_tagline": {"uz": "Logistika bo‘yicha ta’lim resursi.", "ru": "Учебный ресурс по логистике.", "en": "An educational resource for logistics."},
    "about": {"uz": "Loyiha haqida", "ru": "О проекте", "en": "About"},
    "educational_resource": {"uz": "Ta’lim resursi", "ru": "Образовательный ресурс", "en": "Educational resource"},
    "start_learning": {"uz": "O‘qishni boshlash", "ru": "Начать обучение", "en": "Start learning"},
    "learning_materials": {"uz": "O‘quv materiallari", "ru": "Учебные материалы", "en": "Learning materials"},
    "search": {"uz": "Qidirish", "ru": "Найти", "en": "Search"},
    "all": {"uz": "Barchasi", "ru": "Все", "en": "All"},
    "section": {"uz": "Bo‘lim", "ru": "Раздел", "en": "Section"},
    "open": {"uz": "Ochish", "ru": "Открыть", "en": "Open"},
    "download": {"uz": "Yuklab olish", "ru": "Скачать", "en": "Download"},
    "watch_video": {"uz": "Videoni ko‘rish", "ru": "Смотреть видео", "en": "Watch video"},
    "start_test": {"uz": "Testni boshlash", "ru": "Начать тест", "en": "Start test"},
    "back_to_tests": {"uz": "Testlar ro‘yxatiga", "ru": "К списку тестов", "en": "Back to tests"},
    "complete_check": {"uz": "Yakunlash va tekshirish", "ru": "Завершить и проверить", "en": "Finish and check"},
    "save": {"uz": "Saqlash", "ru": "Сохранить", "en": "Save"},
    "cancel": {"uz": "Bekor qilish", "ru": "Отмена", "en": "Cancel"},
    "delete": {"uz": "O‘chirish", "ru": "Удалить", "en": "Delete"},
    "edit": {"uz": "Tahrirlash", "ru": "Изменить", "en": "Edit"},
    "create_topic": {"uz": "Mavzu yaratish", "ru": "Создать тему", "en": "Create topic"},
    "upload_file": {"uz": "Fayl yuklash", "ru": "Загрузить файл", "en": "Upload file"},
    "manage_topics": {"uz": "Mavzularni boshqarish", "ru": "Управлять темами", "en": "Manage topics"},
    "full_admin": {"uz": "To‘liq Django Admin", "ru": "Полный Django Admin", "en": "Full Django Admin"},
    "published": {"uz": "Chop etilgan", "ru": "Опубликовано", "en": "Published"},
    "no_items": {"uz": "Hozircha ma’lumot yo‘q.", "ru": "Пока нет данных.", "en": "No items yet."},
    "library_heading": {"uz": "O‘quv materiallari", "ru": "Учебные материалы", "en": "Learning materials"},
    "library_intro": {"uz": "O‘qituvchi chop etgan hujjatlar, taqdimotlar, jadvallar va videomateriallar.", "ru": "Документы, презентации, таблицы и видеоматериалы, опубликованные преподавателем.", "en": "Documents, presentations, tables and videos published by the instructor."},
    "documents": {"uz": "Hujjatlar va materiallar", "ru": "Документы и материалы", "en": "Documents and materials"},
    "videos": {"uz": "Videolar", "ru": "Видеоматериалы", "en": "Videos"},
    "no_files": {"uz": "Chop etilgan fayllar yo‘q.", "ru": "Опубликованных файлов пока нет.", "en": "There are no published files yet."},
    "no_videos": {"uz": "Chop etilgan videolar yo‘q.", "ru": "Опубликованных видео пока нет.", "en": "There are no published videos yet."},
    "no_video_source": {"uz": "Video manbasi mavjud emas.", "ru": "Источник видео не добавлен.", "en": "No video source is available."},
    "unsupported_video": {"uz": "Bu video formati brauzerda qo‘llab-quvvatlanmaydi. MP4 (H.264) yoki WebM dan foydalaning.", "ru": "Этот формат видео может не поддерживаться браузером. Используйте MP4 (H.264) или WebM.", "en": "This video format may not be supported by your browser. Use MP4 (H.264) or WebM."},
    "browser_no_video": {"uz": "Brauzeringiz ushbu videoni ijro eta olmaydi.", "ru": "Браузер не может воспроизвести это видео.", "en": "Your browser cannot play this video."},
    "external_video": {"uz": "Tashqi videoni ochish", "ru": "Открыть видео на сайте источника", "en": "Open video at source"},
    "open_pdf": {"uz": "PDF hujjatni ochish", "ru": "Открыть PDF документ", "en": "Open PDF document"},
    "download_file": {"uz": "Faylni yuklab olish", "ru": "Скачать файл", "en": "Download file"},
    "knowledge_check": {"uz": "Bilimlarni tekshirish", "ru": "Контроль знаний", "en": "Knowledge check"},
    "quiz_intro": {"uz": "Javoblar urinish tugagach serverda tekshiriladi.", "ru": "Ответы проверяются на сервере после завершения попытки.", "en": "Answers are checked on the server after the attempt is submitted."},
    "question_count": {"uz": "savol", "ru": "вопросов", "en": "questions"},
    "minutes": {"uz": "daq.", "ru": "мин.", "en": "min."},
    "attempts": {"uz": "urinish", "ru": "попыток", "en": "attempts"},
    "published_tests_empty": {"uz": "Chop etilgan testlar yo‘q.", "ru": "Опубликованных тестов пока нет.", "en": "There are no published tests yet."},
    "test_title": {"uz": "Test", "ru": "Тест", "en": "Test"},
    "assessment": {"uz": "Bilimlarni baholash", "ru": "Тестирование", "en": "Assessment"},
    "remaining": {"uz": "Qoldi:", "ru": "Осталось:", "en": "Remaining:"},
    "multiple_choice": {"uz": "Bir nechta javobni tanlash mumkin", "ru": "Можно выбрать несколько вариантов", "en": "Select all that apply"},
    "single_choice": {"uz": "Bitta javobni tanlang", "ru": "Выберите один вариант", "en": "Select one answer"},
    "finish_check": {"uz": "Yakunlash va tekshirish", "ru": "Завершить и проверить", "en": "Finish and check"},
    "correct_answers": {"uz": "To‘g‘ri javoblar:", "ru": "Правильных ответов:", "en": "Correct answers:"},
    "correct": {"uz": "To‘g‘ri", "ru": "Верно", "en": "Correct"},
    "review_answer": {"uz": "Javobni qayta ko‘rib chiqing", "ru": "Проверьте ответ", "en": "Review your answer"},
    "your_choice": {"uz": "Sizning javobingiz:", "ru": "Ваш выбор:", "en": "Your answer:"},
    "no_answer": {"uz": "Javob berilmagan", "ru": "нет ответа", "en": "No answer"},
    "correct_answer": {"uz": "To‘g‘ri javob:", "ru": "Правильный ответ:", "en": "Correct answer:"},
    "topic": {"uz": "Mavzu", "ru": "Тема", "en": "Topic"},
    "course_goals": {"uz": "Ta’lim maqsadlari", "ru": "Цели обучения", "en": "Learning objectives"},
    "supplementary_material": {"uz": "Qo‘shimcha o‘quv materiali", "ru": "Дополнительный учебный материал", "en": "Supplementary learning material"},
    "theory": {"uz": "Nazariy qism", "ru": "Теоретическая часть", "en": "Theory"},
    "practice_task_later": {"uz": "Amaliy topshiriq keyinroq qo‘shiladi.", "ru": "Практическое задание появится позднее.", "en": "A practice task will be added later."},
    "materials_assessment": {"uz": "Materiallar va nazorat", "ru": "Материалы и контроль", "en": "Materials and assessment"},
    "self_check": {"uz": "O‘zini tekshirish savollari", "ru": "Вопросы для самопроверки", "en": "Self-check questions"},
    "on_page": {"uz": "Sahifada", "ru": "На странице", "en": "On this page"},
    "goals": {"uz": "Maqsadlar", "ru": "Цели", "en": "Goals"},
    "resource": {"uz": "Resurslar", "ru": "Ресурсы", "en": "Resources"},
    "about_description": {"uz": "Logistika jarayonlarini boshqarishni o‘rganish uchun raqamli ta’lim resursi.", "ru": "Цифровой образовательный ресурс для изучения управления логистическими процессами.", "en": "A digital learning resource for studying logistics process management."},
    "about_purpose": {"uz": "Maqsad", "ru": "Назначение", "en": "Purpose"},
    "about_learning": {"uz": "Ta’lim qanday tashkil qilingan", "ru": "Как устроено обучение", "en": "How learning works"},
    "module_hours": {"uz": "Resurs nazariya, mustaqil amaliyot, materiallar, videolar, testlar va atamalar lug‘atini birlashtiradi. O‘quv moduli 54 soat: 16 soat nazariya, 24 soat amaliy va laboratoriya mashg‘ulotlari, 14 soat mustaqil ta’lim.", "ru": "Ресурс объединяет теорию, самостоятельную практику, материалы, видео, тесты и словарь терминов. Учебный модуль рассчитан на 54 часа: 16 часов теории, 24 часа практических и лабораторных занятий и 14 часов самостоятельного обучения.", "en": "The resource combines theory, independent practice, materials, videos, tests and a glossary. The 54-hour module includes 16 hours of theory, 24 hours of practical and laboratory sessions, and 14 hours of independent study."},
    "study_steps": {"uz": "Mavzuni oching, materiallarni o‘rganing, topshiriqni bajaring va testdan o‘ting. Administrator boshqaruv panelida tarkibni qo‘shishi va chop etishi mumkin.", "ru": "Откройте тему, изучите материалы, выполните задание и пройдите тест. Администратор может добавлять и публиковать содержание через панель управления.", "en": "Open a topic, study its materials, complete a task and take a test. An administrator can add and publish content through the dashboard."},
    "dashboard_title": {"uz": "Administrator paneli", "ru": "Панель администратора", "en": "Administrator dashboard"},
    "content_management": {"uz": "Tarkibni boshqarish", "ru": "Управление содержанием", "en": "Content management"},
    "changes_saved": {"uz": "O‘zgarishlar bazada saqlanadi va chop etilgach saytda ko‘rinadi.", "ru": "Изменения сохраняются в базе и отображаются на сайте после публикации.", "en": "Changes are saved in the database and appear on the site after publication."},
    "latest_results": {"uz": "So‘nggi natijalar", "ru": "Последние результаты", "en": "Latest results"},
    "user": {"uz": "Foydalanuvchi", "ru": "Пользователь", "en": "User"},
    "date": {"uz": "Sana", "ru": "Дата", "en": "Date"},
    "no_attempts": {"uz": "Hali urinishlar yo‘q.", "ru": "Попыток ещё нет.", "en": "There are no attempts yet."},
    "content": {"uz": "Tarkib", "ru": "Содержание", "en": "Content"},
    "status": {"uz": "Holat", "ru": "Статус", "en": "Status"},
    "order": {"uz": "Tartib", "ru": "Порядок", "en": "Order"},
    "no_topics": {"uz": "Hozircha mavzular yo‘q.", "ru": "Тем пока нет.", "en": "There are no topics yet."},
    "confirmation": {"uz": "Tasdiqlash", "ru": "Подтверждение", "en": "Confirmation"},
    "delete_topic_confirmation": {"uz": "Mavzu bilan bog‘liq yozuvlar ham o‘chirilishi mumkin.", "ru": "Связанные записи могут быть удалены вместе с темой.", "en": "Related records may also be deleted with this topic."},
    "cookie_title": {"uz": "Cookie sozlamalari", "ru": "Настройки cookie", "en": "Cookie preferences"},
    "cookie_copy": {"uz": "Sayt tilni saqlash va xavfsizlik uchun zarur cookie fayllardan foydalanadi. Tanlovingizni saqlash uchun cookie ishlatamiz; tahlil cookie fayllari yo‘q.", "ru": "Сайт использует необходимые cookie для языка и безопасности. Мы сохраняем ваш выбор cookie; аналитические cookie не используются.", "en": "This site uses essential cookies for language and security. A cookie stores your preference; analytics cookies are not used."},
    "accept": {"uz": "Qabul qilish", "ru": "Принять", "en": "Accept"},
    "reject_optional": {"uz": "Faqat zarur", "ru": "Только необходимые", "en": "Essential only"},
    "hero_title": {"uz": "Logistika — amaliyotda qo‘llang.", "ru": "Логистика, которую можно применять.", "en": "Logistics you can put into practice."},
    "hero_intro": {"uz": "Ta’minot zanjirlari, transport, ombor operatsiyalari va KPI boshqaruvini yagona tushunarli yo‘nalishda o‘rganing.", "ru": "Изучайте цепочки поставок, транспорт, складские операции и управление KPI в одном понятном маршруте.", "en": "Study supply chains, transport, warehouse operations and KPI management in one clear learning path."},
    "course_areas": {"uz": "Ta’lim yo‘nalishlari", "ru": "Учебные направления", "en": "Learning areas"},
    "system_to_result": {"uz": "Tizimdan natijagacha", "ru": "От системы до результата", "en": "From system to result"},
    "all_topics_arrow": {"uz": "Barcha mavzular →", "ru": "Все темы →", "en": "All topics →"},
    "study_arrow": {"uz": "O‘rganish →", "ru": "Изучить →", "en": "Study →"},
    "new_materials": {"uz": "Yangi materiallar", "ru": "Новые материалы", "en": "New materials"},
    "open_catalog": {"uz": "Katalogni ochish →", "ru": "Открыть каталог →", "en": "Open catalogue →"},
    "no_topics_match": {"uz": "So‘rovingiz bo‘yicha mavzular topilmadi.", "ru": "По вашему запросу тем нет.", "en": "No topics match your search."},
    "program": {"uz": "Dastur", "ru": "Программа", "en": "Programme"},
    "topics_intro": {"uz": "Materiallar logistika faoliyatining to‘liq sikli asosida tuzilgan.", "ru": "Материалы организованы вокруг полного цикла логистической деятельности.", "en": "Materials follow the full logistics activity cycle."},
    "search_topic": {"uz": "Mavzu yoki tushuncha", "ru": "Тема или понятие", "en": "Topic or concept"},
    "all_sections": {"uz": "Barcha bo‘limlar", "ru": "Все разделы", "en": "All sections"},
    "catalog": {"uz": "Katalog", "ru": "Каталог", "en": "Catalogue"},
    "lecture_intro": {"uz": "Mavzularga bog‘langan tuzilgan qo‘shimcha materiallar.", "ru": "Структурированные дополнительные материалы, связанные с учебными темами.", "en": "Structured supplementary materials linked to the learning topics."},
    "no_lectures": {"uz": "Chop etilgan ma’ruzalar yo‘q.", "ru": "Опубликованных лекций пока нет.", "en": "There are no published lectures yet."},
    "practice_intro": {"uz": "Transport zanjirlari, operatsiyalar va xarajatlarni tahlil qilish topshiriqlari.", "ru": "Задания по анализу транспортных цепочек, операциям и затратам.", "en": "Tasks for analysing transport chains, operations and costs."},
    "no_practice": {"uz": "Chop etilgan topshiriqlar yo‘q.", "ru": "Опубликованных заданий пока нет.", "en": "There are no published tasks yet."},
    "no_matching_terms": {"uz": "Atamalar topilmadi.", "ru": "Термины не найдены.", "en": "No terms found."},
    "enter_term": {"uz": "Atamani kiriting", "ru": "Введите термин", "en": "Enter a term"},
    "empty_search": {"uz": "Hech narsa topilmadi.", "ru": "Ничего не найдено.", "en": "Nothing found."},
    "video_tag": {"uz": "VIDEO", "ru": "ВИДЕО", "en": "VIDEO"},
    "watch_video_arrow": {"uz": "Videoni ko‘rish →", "ru": "Смотреть видео →", "en": "Watch video →"},
    "download_size": {"uz": "Yuklab olish", "ru": "Скачать", "en": "Download"},
    "sign_in_error": {"uz": "Foydalanuvchi nomi va parolni tekshiring.", "ru": "Проверьте имя пользователя и пароль.", "en": "Check your username and password."},
    "username": {"uz": "Foydalanuvchi nomi", "ru": "Имя пользователя", "en": "Username"},
    "password": {"uz": "Parol", "ru": "Пароль", "en": "Password"},
    "admin_accounts_only": {"uz": "Hisobni administrator yaratadi. Ochiq ro‘yxatdan o‘tish mavjud emas.", "ru": "Учётную запись создаёт администратор. Публичной регистрации нет.", "en": "Accounts are created by an administrator. Public registration is unavailable."},
    "login_heading": {"uz": "Tizimga kirish", "ru": "Войти", "en": "Sign in"},
    "no_published_materials": {"uz": "Chop etilgan materiallar yo‘q.", "ru": "Опубликованных материалов пока нет.", "en": "There are no published materials yet."},
    "warehouse": {"uz": "Ombor", "ru": "Склад", "en": "Warehouse"},
    "transport": {"uz": "Transport", "ru": "Транспорт", "en": "Transport"},
    "customer": {"uz": "Mijoz", "ru": "Клиент", "en": "Customer"},
    "hero_visual": {"uz": "Yuk harakati sxemasi", "ru": "Схема движения груза", "en": "Cargo flow diagram"},
    "your_path": {"uz": "Sizning yo‘nalishingiz", "ru": "Ваш маршрут", "en": "Your learning path"},
    "general_material": {"uz": "Umumiy material", "ru": "Общий материал", "en": "General material"},
    "terms": {"uz": "Atamalar", "ru": "Термины", "en": "Terms"},
    "glossary_intro": {"uz": "Logistikaning asosiy tushunchalariga qisqa ta’riflar.", "ru": "Краткие определения ключевых понятий логистики.", "en": "Brief definitions of key logistics concepts."},
    "account_access": {"uz": "Hisobga kirish", "ru": "Доступ к системе", "en": "Account access"},
    "result": {"uz": "Natija", "ru": "Результат", "en": "Result"},
    "all_lectures": {"uz": "Barcha ma’ruzalar", "ru": "Лекции", "en": "Lectures"},
    "skills_training": {"uz": "Ko‘nikmalar mashqi", "ru": "Тренировка навыков", "en": "Skills practice"},
    "practice_intro_text": {"uz": "Transport zanjirlari, operatsiyalar va xarajatlarni tahlil qilish topshiriqlari.", "ru": "Задания по анализу транспортных цепочек, операциям и затратам.", "en": "Tasks for analysing transport chains, operations and costs."},
    "hint": {"uz": "Maslahat", "ru": "Подсказка", "en": "Hint"},
    "topic_breadcrumb": {"uz": "Mavzular", "ru": "Темы", "en": "Topics"},
    "logistics": {"uz": "Logistika", "ru": "Логистика", "en": "Logistics"},
    "practice": {"uz": "Amaliyot", "ru": "Практика", "en": "Practice"},
    "theory_heading": {"uz": "Nazariy qism", "ru": "Теоретическая часть", "en": "Theory"},
    "no_practice_task": {"uz": "Amaliy topshiriq keyinroq qo‘shiladi.", "ru": "Практическое задание появится позднее.", "en": "A practice task will be added later."},
    "video_support_hint": {"uz": "MP4 H.264 yoki WebM brauzeringizga mos keladi.", "ru": "MP4 H.264 или WebM обычно совместимы с браузерами.", "en": "MP4 H.264 or WebM are commonly supported by browsers."},
    "view_material": {"uz": "Materialni ko‘rish", "ru": "Открыть материал", "en": "View material"},
    "about_heading": {"uz": "LogiLearn haqida", "ru": "О проекте", "en": "About LogiLearn"},
    "learning_directions": {"uz": "Ta’lim yo‘nalishlari", "ru": "Учебные направления", "en": "Learning areas"},
    "dashboard_topics": {"uz": "O‘quv mavzulari", "ru": "Учебные темы", "en": "Learning topics"},
    "create_topic": {"uz": "Mavzu yaratish", "ru": "Создать тему", "en": "Create topic"},
    "upload_material": {"uz": "Fayl yuklash", "ru": "Загрузить файл", "en": "Upload file"},
    "manage_topics": {"uz": "Mavzularni boshqarish", "ru": "Управлять темами", "en": "Manage topics"},
    "full_admin": {"uz": "To‘liq Django Admin", "ru": "Полный Django Admin", "en": "Full Django Admin"},
    "recent_attempts": {"uz": "so‘nggi urinishlar", "ru": "последних попыток", "en": "recent attempts"},
    "topic_count": {"uz": "mavzular", "ru": "тем", "en": "topics"},
    "material_count": {"uz": "materiallar", "ru": "материалов", "en": "materials"},
    "topic_name": {"uz": "Mavzu", "ru": "Тема", "en": "Topic"},
    "section": {"uz": "Bo‘lim", "ru": "Раздел", "en": "Section"},
    "topic_order": {"uz": "Tartib", "ru": "Порядок", "en": "Order"},
    "edit": {"uz": "Tahrirlash", "ru": "Изменить", "en": "Edit"},
    "delete": {"uz": "O‘chirish", "ru": "Удалить", "en": "Delete"},
    "cancel": {"uz": "Bekor qilish", "ru": "Отмена", "en": "Cancel"},
    "delete_confirmation": {"uz": "Mavzu bilan bog‘liq yozuvlar ham o‘chirilishi mumkin.", "ru": "Связанные записи могут быть удалены вместе с темой.", "en": "Related records may also be deleted with this topic."},
    "save": {"uz": "Saqlash", "ru": "Сохранить", "en": "Save"},
    "form_dashboard": {"uz": "Boshqaruv paneli", "ru": "Панель управления", "en": "Dashboard"},
    "create_new_topic": {"uz": "Yangi mavzu", "ru": "Новая тема", "en": "New topic"},
    "edit_topic": {"uz": "Mavzuni tahrirlash", "ru": "Редактирование темы", "en": "Edit topic"},
    "upload_material_title": {"uz": "Material yuklash", "ru": "Загрузка материала", "en": "Upload material"},
    "no_quiz_yet": {"uz": "Chop etilgan testlar yo‘q.", "ru": "Опубликованных тестов пока нет.", "en": "There are no published tests yet."},
    "website_logo": {"uz": "Logotip", "ru": "Логотип", "en": "Logo"},
    "lecture_tag": {"uz": "MA’RUZA", "ru": "ЛЕКЦИЯ", "en": "LECTURE"},
    "open_topic_arrow": {"uz": "Mavzuni ochish →", "ru": "Открыть тему →", "en": "Open topic →"},
    "studied": {"uz": "O‘rganildi", "ru": "Изучено", "en": "Studied"},
    "mark_studied": {"uz": "O‘rganilgan deb belgilash", "ru": "Отметить как изученное", "en": "Mark as studied"},
    "check_knowledge": {"uz": "Bilimlarni tekshirish", "ru": "Проверить знания", "en": "Check your knowledge"},
    "knowledge_check": {"uz": "Bilimlarni tekshirish", "ru": "Контроль знаний", "en": "Knowledge check"},
    "quiz_intro": {"uz": "Javoblar urinish yakunlangach serverda tekshiriladi.", "ru": "Ответы проверяются на сервере после завершения попытки.", "en": "Answers are checked on the server after submission."},
    "question_count": {"uz": "savol", "ru": "вопросов", "en": "questions"},
    "minutes": {"uz": "daq.", "ru": "мин.", "en": "min."},
    "attempts": {"uz": "urinish", "ru": "попыток", "en": "attempts"},
    "published_tests_empty": {"uz": "Chop etilgan testlar yo‘q.", "ru": "Опубликованных тестов пока нет.", "en": "There are no published tests yet."},
    "assessment": {"uz": "Bilimlarni baholash", "ru": "Тестирование", "en": "Assessment"},
    "remaining": {"uz": "Qoldi:", "ru": "Осталось:", "en": "Remaining:"},
    "multiple_choice": {"uz": "Bir nechta javobni tanlash mumkin", "ru": "Можно выбрать несколько вариантов", "en": "Select all that apply"},
    "single_choice": {"uz": "Bitta javobni tanlang", "ru": "Выберите один вариант", "en": "Select one answer"},
    "finish_check": {"uz": "Yakunlash va tekshirish", "ru": "Завершить и проверить", "en": "Finish and check"},
    "correct_answers": {"uz": "To‘g‘ri javoblar:", "ru": "Правильных ответов:", "en": "Correct answers:"},
    "correct": {"uz": "To‘g‘ri", "ru": "Верно", "en": "Correct"},
    "review_answer": {"uz": "Javobni tekshiring", "ru": "Проверьте ответ", "en": "Review answer"},
    "your_choice": {"uz": "Sizning javobingiz:", "ru": "Ваш выбор:", "en": "Your answer:"},
    "no_answer": {"uz": "Javob yo‘q", "ru": "нет ответа", "en": "No answer"},
    "correct_answer": {"uz": "To‘g‘ri javob:", "ru": "Правильный ответ:", "en": "Correct answer:"},
    "library_heading": {"uz": "O‘quv materiallari", "ru": "Учебные материалы", "en": "Learning materials"},
    "library_intro": {"uz": "Hujjatlar, taqdimotlar, jadvallar va videolar.", "ru": "Документы, презентации, таблицы и видео.", "en": "Documents, presentations, tables and videos."},
    "documents": {"uz": "Hujjatlar va materiallar", "ru": "Документы и материалы", "en": "Documents and materials"},
    "videos": {"uz": "Videolar", "ru": "Видеоматериалы", "en": "Videos"},
    "no_files": {"uz": "Chop etilgan fayllar yo‘q.", "ru": "Опубликованных файлов пока нет.", "en": "There are no published files yet."},
    "no_videos": {"uz": "Chop etilgan videolar yo‘q.", "ru": "Опубликованных видео пока нет.", "en": "There are no published videos yet."},
    "no_video_source": {"uz": "Video manbasi yo‘q.", "ru": "Источник видео не добавлен.", "en": "No video source is available."},
    "browser_no_video": {"uz": "Brauzer ushbu videoni ijro eta olmaydi.", "ru": "Браузер не может воспроизвести это видео.", "en": "Your browser cannot play this video."},
    "unsupported_video": {"uz": "Brauzer qo‘llamasa, MP4 (H.264) yoki WebM formatidan foydalaning.", "ru": "Если браузер не поддерживает файл, используйте MP4 (H.264) или WebM.", "en": "If playback is unsupported, use MP4 (H.264) or WebM."},
    "external_video": {"uz": "Manba saytida ochish", "ru": "Открыть на сайте источника", "en": "Open at source"},
    "download_file": {"uz": "Faylni yuklab olish", "ru": "Скачать файл", "en": "Download file"},
    "accept": {"uz": "Qabul qilish", "ru": "Принять", "en": "Accept"},
    "reject_optional": {"uz": "Faqat zarur", "ru": "Только необходимые", "en": "Essential only"},
    "cookie_title": {"uz": "Cookie sozlamalari", "ru": "Настройки cookie", "en": "Cookie preferences"},
    "cookie_copy": {"uz": "Til, sessiya va xavfsizlik uchun zarur cookie fayllardan foydalanamiz. Tanlovingiz cookie orqali saqlanadi; kuzatuv cookie fayllari ishlatilmaydi.", "ru": "Используем необходимые cookie для языка, сессии и безопасности. Ваш выбор сохраняется в cookie; cookie отслеживания не используются.", "en": "We use essential cookies for language, sessions and security. Your preference is stored in a cookie; tracking cookies are not used."},
    "topic_saved": {"uz": "Mavzu saqlandi.", "ru": "Тема сохранена.", "en": "Topic saved."},
    "topic_deleted": {"uz": "Mavzu o‘chirildi.", "ru": "Тема удалена.", "en": "Topic deleted."},
    "material_uploaded": {"uz": "Material yuklandi.", "ru": "Материал загружен.", "en": "Material uploaded."},
    "attempt_limit": {"uz": "Urinishlar soni tugadi.", "ru": "Лимит попыток исчерпан.", "en": "You have reached the attempt limit."},
    "time_expired": {"uz": "Vaqt tugadi. Urinish hisoblanmadi.", "ru": "Время истекло. Попытка не засчитана.", "en": "Time expired. The attempt was not scored."},
    "manage_tests": {"uz": "Testlarni boshqarish", "ru": "Управление тестами", "en": "Manage tests"},
    "create_test": {"uz": "Test yaratish", "ru": "Создать тест", "en": "Create test"},
    "edit_test": {"uz": "Testni tahrirlash", "ru": "Редактировать тест", "en": "Edit test"},
    "test_settings": {"uz": "Test sozlamalari", "ru": "Настройки теста", "en": "Test settings"},
    "test_name": {"uz": "Test nomi", "ru": "Название теста", "en": "Test title"},
    "test_description": {"uz": "Tavsif", "ru": "Описание", "en": "Description"},
    "publish_test": {"uz": "Testni chop etish", "ru": "Опубликовать тест", "en": "Publish test"},
    "questions": {"uz": "Savollar", "ru": "Вопросы", "en": "Questions"},
    "question": {"uz": "Savol", "ru": "Вопрос", "en": "Question"},
    "answer_options": {"uz": "Javob variantlari", "ru": "Варианты ответа", "en": "Answer options"},
    "correct_answer": {"uz": "To‘g‘ri javob", "ru": "Правильный ответ", "en": "Correct answer"},
    "add_question": {"uz": "Savol qo‘shish", "ru": "Добавить вопрос", "en": "Add question"},
    "add_answer": {"uz": "Javob qo‘shish", "ru": "Добавить вариант", "en": "Add answer"},
    "remove": {"uz": "Olib tashlash", "ru": "Удалить", "en": "Remove"},
    "save_test": {"uz": "Testni saqlash", "ru": "Сохранить тест", "en": "Save test"},
}

@register.simple_tag(takes_context=True)
def ui(context, key):
    language = (get_language() or "uz").split("-")[0]
    values = TEXT.get(key, {})
    return values.get(language, values.get("uz", key))

@register.filter
def can_view_dashboard(user):
    return bool(user and user.is_active and user.is_staff and (
        user.is_superuser or user.has_perm("courses.view_topic") or user.has_perm("materials.view_material")
    ))

def translate_ui(key, language=None):
    active_language = (language or get_language() or "uz").split("-")[0]
    values = TEXT.get(key, {})
    return values.get(active_language, values.get("uz", key))


# Only the six built-in course topics are translated here.  Content created by
# an administrator keeps its original wording, so switching the interface
# language never changes user-authored material.
BUILTIN_TOPIC_TEXT = {
    "supply-chain": {
        "title": {"uz": "Logistika tizimi va ta’minot zanjiri", "en": "Logistics System and Supply Chain"},
        "summary": {"uz": "Yetkazib beruvchilar, operatsiyalar va iste’molchilarni yagona oqimda bog‘lash.", "en": "Connecting suppliers, operations and customers in one flow."},
        "objectives": {"uz": "Ta’minot zanjiri ishtirokchilarini aniqlash va moddiy, axborot hamda moliyaviy oqimlar harakatini tavsiflash.", "en": "Identify supply-chain participants and describe the movement of material, information and financial flows."},
    },
    "logistics-processes": {
        "title": {"uz": "Logistika jarayonlari va ularning o‘zaro bog‘liqligi", "en": "Logistics Processes and Their Interconnection"},
        "summary": {"uz": "Rejalashtirish, xarid, tashish, omborlash va taqsimlash.", "en": "Planning, procurement, transportation, warehousing and distribution."},
        "objectives": {"uz": "Jarayonlarning o‘zaro bog‘liqligini tushunish va mas’uliyat topshiriladigan nuqtalarni topish.", "en": "Understand process interdependencies and identify responsibility handover points."},
    },
    "transport-chain": {
        "title": {"uz": "Transport zanjiri tahlili", "en": "Transport Chain Analysis"},
        "summary": {"uz": "Yo‘nalish, muddat, xavf va tashish xarajatlarini baholash.", "en": "Assessing routes, lead times, risks and transportation costs."},
        "objectives": {"uz": "Tashish variantlarini muddat, qiymat va xavf bo‘yicha solishtirish.", "en": "Compare transport options by lead time, cost and risk."},
    },
    "warehouse-inventory": {
        "title": {"uz": "Ombor, zaxiralar va taqsimlash", "en": "Warehousing, Inventory and Distribution"},
        "summary": {"uz": "Ombor operatsiyalari va zaxira darajasini rejalashtirish.", "en": "Planning warehouse operations and inventory levels."},
        "objectives": {"uz": "Zaxiralar va ombor operatsiyalarini nazorat qilish ko‘rsatkichlarini tanlash.", "en": "Choose indicators for monitoring inventory and warehouse operations."},
    },
    "operations-kpi": {
        "title": {"uz": "Operatsiyalar va KPI boshqaruvi", "en": "Operations Management and KPIs"},
        "summary": {"uz": "Logistika operatsiyalari bajarilishini o‘lchab bo‘ladigan ko‘rsatkichlar orqali kuzatish.", "en": "Monitoring logistics operations through measurable indicators."},
        "objectives": {"uz": "Jarayon ishining asosiy ko‘rsatkichlarini hisoblash va talqin qilish.", "en": "Calculate and interpret core process performance indicators."},
    },
    "optimization-efficiency": {
        "title": {"uz": "Optimallashtirish va samaradorlik", "en": "Optimisation and Efficiency"},
        "summary": {"uz": "Xarajatlar, resurslar va xizmat darajasini yaxshilash yo‘llarini izlash.", "en": "Finding improvements in cost, resources and service level."},
        "objectives": {"uz": "Ma’lumotlar asosida optimallashtirish choralarini asoslash.", "en": "Justify optimisation measures using data."},
    },
}

BUILTIN_TEXT = {
    "Основы логистики": {"uz": "Logistika asoslari", "en": "Logistics Fundamentals"},
    "Дополнительный учебный материал. Логистическая задача рассматривается как управление взаимосвязанными потоками. Для обоснованного решения определите участников процесса, границы операции, измеряемый результат и ограничения.": {
        "uz": "Qo‘shimcha o‘quv materiali. Logistika vazifasi o‘zaro bog‘langan oqimlarni boshqarish sifatida qaraladi. Asosli qaror uchun jarayon ishtirokchilari, operatsiya chegaralari, o‘lchanadigan natija va cheklovlarni aniqlang.",
        "en": "Supplementary learning material. A logistics task is considered as managing interconnected flows. For a sound decision, identify the process participants, operation boundaries, measurable result and constraints.",
    },
    "Qaysi ishtirokchilar jarayonga kiradi?\nQaysi ko‘rsatkichlar natijani tasdiqlaydi?\nQaysi xavflarni hisobga olish kerak?": {
        "uz": "Qaysi ishtirokchilar jarayonga kiradi?\nQaysi ko‘rsatkichlar natijani tasdiqlaydi?\nQaysi xavflarni hisobga olish kerak?",
        "en": "Which participants are involved in the process?\nWhich indicators confirm the result?\nWhich risks should be considered?",
    },
    "Какие участники входят в процесс?\nКакие показатели подтвердят результат?\nКакие риски следует учесть?": {
        "uz": "Qaysi ishtirokchilar jarayonga kiradi?\nQaysi ko‘rsatkichlar natijani tasdiqlaydi?\nQaysi xavflarni hisobga olish kerak?",
        "en": "Which participants are involved in the process?\nWhich indicators confirm the result?\nWhich risks should be considered?",
    },
    "Кейс для анализа": {"uz": "Tahlil uchun keys", "en": "Case for Analysis"},
    "Выберите знакомую поставку или операцию. Опишите участников, этапы, риски, показатели срока и стоимости.": {
        "uz": "Tanish yetkazib berish yoki operatsiyani tanlang. Ishtirokchilar, bosqichlar, xavflar, muddat va qiymat ko‘rsatkichlarini tavsiflang.",
        "en": "Choose a familiar delivery or operation. Describe its participants, stages, risks, lead-time and cost indicators.",
    },
    "Начните со схемы «поставщик — операция — получатель».": {"uz": "«Yetkazib beruvchi — operatsiya — qabul qiluvchi» sxemasidan boshlang.", "en": "Start with the 'supplier — operation — recipient' diagram."},
    "Дополнительный материал для самостоятельного чтения. Используйте тему как опорную структуру для анализа реальной операции.": {
        "uz": "Mustaqil o‘qish uchun qo‘shimcha material. Mavzudan haqiqiy operatsiyani tahlil qilish uchun tayanch tuzilma sifatida foydalaning.",
        "en": "Supplementary reading. Use the topic as a framework for analysing a real operation.",
    },
    "Самопроверка: основы логистики": {"uz": "O‘zini tekshirish: logistika asoslari", "en": "Self-check: Logistics Fundamentals"},
    "Короткий тест по базовым понятиям.": {"uz": "Asosiy tushunchalar bo‘yicha qisqa test.", "en": "A short test on core concepts."},
    "Что объединяет цепочка поставок?": {"uz": "Ta’minot zanjiri nimani birlashtiradi?", "en": "What does a supply chain connect?"},
    "Цепочка поставок связывает организации и процессы, обеспечивающие движение ценности.": {"uz": "Ta’minot zanjiri qiymat harakatini ta’minlaydigan tashkilotlar va jarayonlarni bog‘laydi.", "en": "A supply chain links organisations and processes that enable the movement of value."},
    "Поставщиков, операции и получателей": {"uz": "Yetkazib beruvchilarni, operatsiyalarni va qabul qiluvchilarni", "en": "Suppliers, operations and recipients"},
    "Только складские помещения": {"uz": "Faqat omborxonalarni", "en": "Only warehouses"},
    "Логистика": {"uz": "Logistika", "en": "Logistics"},
    "Управление потоками ресурсов и связанной информацией от источника к потребителю.": {"uz": "Resurslar va ular bilan bog‘liq axborot oqimlarini manbadan iste’molchigacha boshqarish.", "en": "Management of resource flows and related information from source to consumer."},
    "Цепочка поставок": {"uz": "Ta’minot zanjiri", "en": "Supply Chain"},
    "Сеть организаций и процессов, обеспечивающих создание и доставку продукта.": {"uz": "Mahsulotni yaratish va yetkazib berishni ta’minlaydigan tashkilotlar va jarayonlar tarmog‘i.", "en": "A network of organisations and processes that creates and delivers a product."},
    "Измеримый показатель, который используют для оценки достижения цели.": {"uz": "Maqsadga erishishni baholash uchun ishlatiladigan o‘lchab bo‘ladigan ko‘rsatkich.", "en": "A measurable indicator used to assess goal achievement."},
    "Запас": {"uz": "Zaxira", "en": "Inventory"},
    "Ресурс, хранимый для обеспечения спроса или непрерывности операций.": {"uz": "Talabni qondirish yoki operatsiyalar uzluksizligini ta’minlash uchun saqlanadigan resurs.", "en": "A resource kept to meet demand or maintain continuity of operations."},
    "Распределение": {"uz": "Taqsimlash", "en": "Distribution"},
    "Организация движения готовой продукции к потребителю.": {"uz": "Tayyor mahsulotning iste’molchiga harakatini tashkil etish.", "en": "Organising the movement of finished goods to the consumer."},
}

for _slug, _values in BUILTIN_TOPIC_TEXT.items():
    _russian_title = {
        "supply-chain": "Логистическая система и цепочка поставок",
        "logistics-processes": "Логистические процессы и их взаимосвязь",
        "transport-chain": "Анализ транспортной цепочки",
        "warehouse-inventory": "Склад, запасы и распределение",
        "operations-kpi": "Управление операциями и KPI",
        "optimization-efficiency": "Оптимизация и эффективность",
    }[_slug]
    BUILTIN_TEXT[f"Введение: {_russian_title}"] = {
        "uz": f"Kirish: {_values['title']['uz']}",
        "en": f"Introduction: {_values['title']['en']}",
    }


@register.filter
def topic_text(topic, field):
    """Return a localized built-in topic field, or the database value unchanged."""
    if topic is None:
        return ""
    value = getattr(topic, field, "")
    language = (get_language() or "uz").split("-")[0]
    translated = BUILTIN_TOPIC_TEXT.get(topic.slug, {}).get(field, {}).get(language)
    return translated or BUILTIN_TEXT.get(str(value), {}).get(language, value)


@register.filter
def builtin_text(value):
    """Translate exact strings from the bundled demonstration course only."""
    language = (get_language() or "uz").split("-")[0]
    return BUILTIN_TEXT.get(str(value), {}).get(language, value)

@register.simple_tag(takes_context=True)
def translated_status(context, status):
    language = (get_language() or "uz").split("-")[0]
    labels = {
        "draft": {"uz": "Qoralama", "ru": "Черновик", "en": "Draft"},
        "published": {"uz": "Chop etilgan", "ru": "Опубликовано", "en": "Published"},
        "hidden": {"uz": "Yashirilgan", "ru": "Скрыто", "en": "Hidden"},
    }
    return labels.get(status, {}).get(language, status)
