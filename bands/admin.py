from django.contrib import admin
from .models import Band, BandInvite

# Register your models here.
admin.site.register(Band)
admin.site.register(BandInvite)