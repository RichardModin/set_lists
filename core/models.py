# core/models.py

from django.contrib.auth.models import User
from django.db import models
from bands.models import Band
from songs.models import Song


class SetList(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="setlists")
    name = models.CharField(max_length=100)
    song_ids = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.band.name})"

    @property
    def ordered_songs(self):
        """
        Return Song instances in the order stored in song_ids.
        Falls back to an empty list if song_ids is empty.
        """
        if not self.song_ids:
            return []

        qs = Song.objects.filter(id__in=self.song_ids)
        songs_by_id = {song.id: song for song in qs}
        return [songs_by_id[song_id] for song_id in self.song_ids if song_id in songs_by_id]