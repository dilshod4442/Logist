from django.contrib import admin
from .models import Term
@admin.register(Term)
class TermAdmin(admin.ModelAdmin): list_display = ("term", "letter", "published"); list_filter = ("published", "letter"); search_fields = ("term", "definition")
