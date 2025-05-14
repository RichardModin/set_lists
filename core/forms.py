from django import forms
from .models import Band, SetList, Song
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name']

class SetListForm(forms.ModelForm):
    class Meta:
        model = SetList
        fields = ['name', 'songs']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'key', 'tempo']
