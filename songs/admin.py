from django.contrib import admin
from .models import Song, Notes


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "band", "key", "tempo", "genre", "created_by")
    list_filter = ("band", "genre", "created_by")
    search_fields = ("title", "artist", "band__name")


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ("song", "user", "created_at", "updated_at")
    list_filter = ("song", "user", "created_at")
