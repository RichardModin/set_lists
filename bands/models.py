from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Band(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='bands')
    created_at = models.DateTimeField(auto_now_add=True)

class BandInvite(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)