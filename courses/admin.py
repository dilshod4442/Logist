from django.contrib import admin
from django.utils.html import format_html
from .models import Lecture, PracticeTask, Section, SiteSetting, Topic, TopicProgress


class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 1
    fields = ("title", "body", "order", "published")
    show_change_link = True
    verbose_name = "лекция"
    verbose_name_plural = "лекции"


class PracticeTaskInline(admin.StackedInline):
    model = PracticeTask
    extra = 1
    fields = ("title", "task", "guidance", "published")
    show_change_link = True
    verbose_name = "практическое задание"
    verbose_name_plural = "практические задания"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [LectureInline, PracticeTaskInline]
    list_display = ("title", "section", "status", "order", "created_at", "updated_at")
    list_filter = ("status", "section")
    list_editable = ("status", "order")
    search_fields = ("title", "summary", "theory")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    fieldsets = (
        (None, {
            "fields": ("section", "title", "slug", "status", "order"),
        }),
        ("Содержание", {
            "fields": ("summary", "objectives", "theory", "self_check"),
            "classes": ("wide",),
        }),
    )
    date_hierarchy = "created_at"
    save_on_top = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("section")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "topic_count")
    list_editable = ("order",)
    ordering = ("order",)
    search_fields = ("title",)

    @admin.display(description="тем")
    def topic_count(self, obj):
        return obj.topics.count()


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "order", "published")
    list_filter = ("published", "topic")
    list_editable = ("order", "published")
    search_fields = ("title", "body", "topic__title")
    ordering = ("topic", "order", "title")
    fieldsets = (
        (None, {"fields": ("topic", "title", "order", "published")}),
        ("Содержание", {"fields": ("body",), "classes": ("wide",)}),
    )
    save_on_top = True


@admin.register(PracticeTask)
class PracticeTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "published")
    list_filter = ("published", "topic")
    list_editable = ("published",)
    search_fields = ("title", "task", "topic__title")
    fieldsets = (
        (None, {"fields": ("topic", "title", "published")}),
        ("Задание", {"fields": ("task", "guidance"), "classes": ("wide",)}),
    )
    save_on_top = True


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "tagline")


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "completed_at")
    list_filter = ("topic",)
    search_fields = ("user__username", "topic__title")
    readonly_fields = ("user", "topic", "completed_at")
