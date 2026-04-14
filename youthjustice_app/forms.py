from django import forms
from .models import Program
from django.views.generic import CreateView
from .models import Program

class ProgramCreateView(CreateView):
    model = Program
    fields = [
        "name",
        "region",
        "category",
        "age_min",
        "age_max",
        "short_description",
        "website",
    ]
    template_name = "youthjustice_app/add_program.html"
    success_url = "/programs/"

def form_valid(self, form):
    form.instance.organisation = self.request.user.username  # simple fix
    return super().form_valid(form)
    
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
