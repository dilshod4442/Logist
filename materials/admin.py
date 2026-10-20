from django.contrib import admin
from django.utils.html import format_html
from .models import Material, Video


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "status", "is_public", "extension_tag", "uploaded_at")
    list_filter = ("status", "is_public", "topic")
    list_editable = ("status", "is_public")
    search_fields = ("title", "description", "topic__title")
    ordering = ("-uploaded_at",)
    date_hierarchy = "uploaded_at"
    fieldsets = (
        (None, {
            "fields": ("topic", "title", "description", "status", "is_public"),
        }),
        ("Файл", {
            "fields": ("file",),
            "description": (
                "Разрешены: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, CSV, "
                "JPG, JPEG, PNG, WEBP, ZIP, MP4, WEBM. Максимум 200 МБ."
            ),
        }),
    )
    save_on_top = True

    @admin.display(description="тип")
    def extension_tag(self, obj):
        return obj.extension if obj.file else "—"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "status", "has_file", "has_external", "cover_thumb")
    list_filter = ("status", "topic")
    list_editable = ("status",)
    search_fields = ("title", "description", "topic__title")
    fieldsets = (
        (None, {
            "fields": ("topic", "title", "description", "status"),
        }),
        ("Видео-источник (заполните хотя бы одно)", {
            "fields": ("external_url", "video_file"),
            "description": (
                "external_url — ссылка на YouTube / Vimeo / другой сайт. "
                "video_file — загружаемый файл MP4 или WebM (до 200 МБ)."
            ),
        }),
        ("Обложка", {
            "fields": ("cover",),
            "classes": ("collapse",),
        }),
    )
    save_on_top = True

    @admin.display(description="файл", boolean=True)
    def has_file(self, obj):
        return bool(obj.video_file)

    @admin.display(description="ссылка", boolean=True)
    def has_external(self, obj):
        return bool(obj.external_url)

    @admin.display(description="обложка")
    def cover_thumb(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.cover.url,
            )
        return "—"
