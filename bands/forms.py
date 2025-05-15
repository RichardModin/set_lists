from django import forms
from django.contrib.auth.models import User
from .models import Band, BandInvite

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['name']

class BandInviteForm(forms.ModelForm):
    invited_user = forms.CharField(
        max_length=150,
        help_text="Enter the username of the user you want to invite."
    )

    class Meta:
        model = BandInvite
        fields = ['invited_user']

    def clean_invited_user(self):
        username = self.cleaned_data['invited_user']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No user with this username exists.")
        return user