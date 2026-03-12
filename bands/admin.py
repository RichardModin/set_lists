from django.contrib import admin
from .models import Band, BandInvite


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("members",)


@admin.register(BandInvite)
class BandInviteAdmin(admin.ModelAdmin):
    list_display = ("band", "invited_user", "invited_by", "accepted", "created_at")
    list_filter = ("accepted", "created_at", "band")
    search_fields = ("band__name", "invited_user__username", "invited_by__username")