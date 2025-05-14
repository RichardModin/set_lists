from django.contrib import admin
from .models import Band, Song, SetList, SetListSong, BandInvite

admin.site.register(Band)
admin.site.register(Song)
admin.site.register(SetList)
admin.site.register(SetListSong)
admin.site.register(BandInvite)
