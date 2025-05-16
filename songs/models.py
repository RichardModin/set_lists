from django.contrib.auth.models import User
from django.db import models
from bands.models import Band

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    key = models.CharField(max_length=5, null=True, blank=True)
    tempo = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='songs')
    general_notes = models.TextField(null=True, blank=True)

class Notes(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='note')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.song.title}"