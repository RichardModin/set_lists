from django import forms
from .models import Band

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name']