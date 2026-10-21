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


class Venue(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Event(models.Model):
    EVENT_TYPE_CONCERT = "concert"
    EVENT_TYPE_GENERIC = "generic"

    EVENT_TYPE_CHOICES = [
        (EVENT_TYPE_CONCERT, "Concert"),
        (EVENT_TYPE_GENERIC, "Generic"),
    ]

    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default=EVENT_TYPE_GENERIC)
    date = models.DateField()
    time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    location = models.CharField(max_length=255, null=True, blank=True)
    door_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.title} ({self.get_type_display()}) on {self.date}"


class EventNote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_notes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_notes")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "user"], name="unique_note_per_user_per_event"),
        ]

    def __str__(self):
        return f"Note by {self.user.username} on {self.event.title}"