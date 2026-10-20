from django.contrib import admin
from .models import Lecture, PracticeTask, Section, SiteSetting, Topic, TopicProgress
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "status", "order"); list_filter = ("status", "section"); search_fields = ("title", "summary"); prepopulated_fields = {"slug": ("title",)}; ordering = ("order",)
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin): list_display = ("title", "order"); ordering = ("order",)
admin.site.register([Lecture, PracticeTask, TopicProgress, SiteSetting])
