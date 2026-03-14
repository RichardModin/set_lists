from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import SetList, Event, EventNote


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SetListForm(forms.ModelForm):
    class Meta:
        model = SetList
        fields = ["name"]


class DuplicateSetListForm(forms.ModelForm):
    class Meta:
        model = SetList
        fields = ["name"]
        labels = {
            "name": "New Set List Name",
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "type",
            "date",
            "time",
            "venue",
            "location",
            "door_price",
            "notes",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "venue": forms.Select(attrs={"class": "form-select"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "door_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class EventNoteForm(forms.ModelForm):
    class Meta:
        model = EventNote
        fields = ["content"]