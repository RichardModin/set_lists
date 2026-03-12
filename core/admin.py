from django.contrib import admin
from .models import SetList, SetListSong


@admin.register(SetList)
class SetListAdmin(admin.ModelAdmin):
    list_display = ("name", "band", "created_at")
    list_filter = ("band", "created_at")
    search_fields = ("name", "band__name")


@admin.register(SetListSong)
class SetListSongAdmin(admin.ModelAdmin):
    list_display = ("setlist", "song", "order")
    list_filter = ("setlist", "song")
