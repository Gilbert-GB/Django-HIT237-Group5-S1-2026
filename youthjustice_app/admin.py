from django.contrib import admin
from .models import Organisation, Program, CrimeDataSnapshot, CrimeData, EngagementData


# ORGANISATION ADMIN

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation_type", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("organisation_type",)
