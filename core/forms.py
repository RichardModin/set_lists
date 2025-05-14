from django import forms
from .models import SetList
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SetListForm(forms.ModelForm):
    class Meta:
        model = SetList
        fields = ['name', 'songs']
