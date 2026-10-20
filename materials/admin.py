from django.contrib import admin
from .models import Material, Video
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin): list_display = ("title", "topic", "status", "is_public", "uploaded_at"); list_filter = ("status", "is_public"); search_fields = ("title", "description")
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin): list_display = ("title", "topic", "status"); list_filter = ("status",); search_fields = ("title", "description")
