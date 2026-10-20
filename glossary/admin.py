from django.contrib import admin
from .models import Term


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("term", "letter", "published")
    list_filter = ("published", "letter")
    list_editable = ("published",)
    search_fields = ("term", "definition")
    ordering = ("term",)
    fieldsets = (
        (None, {"fields": ("term", "definition", "published")}),
    )
