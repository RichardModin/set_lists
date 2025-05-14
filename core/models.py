# core/models.py

from django.contrib.auth.models import User
from django.db import models
from bands.models import Band
from songs.models import Song

class SetList(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='setlists')
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song, through='SetListSong')
    created_at = models.DateTimeField(auto_now_add=True)

class SetListSong(models.Model):
    setlist = models.ForeignKey(SetList, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()