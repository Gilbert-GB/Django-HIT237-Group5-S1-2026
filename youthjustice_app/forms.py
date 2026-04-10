# forms.py is used to create Django forms for user input

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import OrganisationProfile, Program


# This form creates a normal Django user with its organisation profile

class OrganisationRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    organisation_name = forms.CharField(max_length=200)
    contact_email = forms.EmailField(required=True)
    contact_phone = forms.CharField(max_length=30, required=False)
    region = forms.ChoiceField(choices=OrganisationProfile.REGION_CHOICES)
