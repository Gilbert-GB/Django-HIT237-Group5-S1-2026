from django import forms
from .models import Program, Organisation


# ORGANISATION FORM

# Useful when we want to create organisations from admin, and UI in final assignment design.
# Not required for public users yet at this stage of our assignment.

class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = [
            "name",
            "organisation_type",
            "email",
            "phone",
            "website",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


# PROGRAM FORM

# Used for both:
# - adding a program
# - editing a program

# Because organisation is now a ForeignKey, this form will show
# a dropdown of organisations.

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            "name",
            "organisation",
            "region",
            "category",
            "age_min",
            "age_max",
            "is_available",
            "is_featured",
            "short_description",
            "website",
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 4}),
            "website": forms.URLInput(attrs={"placeholder": "https://example.com"}),
        }