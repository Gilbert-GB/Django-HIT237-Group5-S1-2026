from django.contrib import admin
from .models import Program

# Models are being registered here
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "category", "is_available")
    list_filter = ("region", "category")
    search_fields = ("name", "organisation")

admin.site.register(Program, ProgramAdmin) 