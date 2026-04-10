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


    # We shall Save user details first, then create its organisation profile
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            OrganisationProfile.objects.create(
                user=user,
                organisation_name=self.cleaned_data["organisation_name"],
                contact_email=self.cleaned_data["contact_email"],
                contact_phone=self.cleaned_data["contact_phone"],
                region=self.cleaned_data["region"],
            )

        return user
    
# This form is for creating/editing program listings
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            "name",
            "region",
            "category",
            "age_min",
            "age_max",
            "is_available",
            "is_featured",
            "short_description",
            "website",
        ]

# This file serves logic, for users to register and manage listings through the website