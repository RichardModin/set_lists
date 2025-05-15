from django import forms
from .models import Band, BandInvite

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name']

class BandInviteForm(forms.ModelForm):
    class Meta:
        model = BandInvite
        fields = ['invited_user']