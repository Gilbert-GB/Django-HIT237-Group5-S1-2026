from django import forms
from .models import Program

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
