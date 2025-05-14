# core/models.py

from django.contrib.auth.models import User
from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='bands')
    created_at = models.DateTimeField(auto_now_add=True)

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    key = models.CharField(max_length=5, null=True, blank=True)
    tempo = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='songs')  # New relationship

class SetList(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='setlists')
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song, through='SetListSong')
    created_at = models.DateTimeField(auto_now_add=True)

class SetListSong(models.Model):
    setlist = models.ForeignKey(SetList, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

class BandInvite(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)