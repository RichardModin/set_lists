from django.contrib import admin
from .models import SetList


@admin.register(SetList)
class SetListAdmin(admin.ModelAdmin):
    list_display = ("name", "band", "created_at")
    list_filter = ("band", "created_at")
    search_fields = ("name", "band__name")
