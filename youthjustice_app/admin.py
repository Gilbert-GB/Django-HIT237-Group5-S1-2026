from django.contrib import admin
from .models import Organisation, Program, CrimeDataSnapshot, CrimeData, EngagementData


# ORGANISATION ADMIN

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation_type", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("organisation_type",)



# PROGRAM ADMIN

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organisation",
        "region",
        "category",
        "is_available",
        "is_featured",
        "created_at",
    )
    search_fields = ("name", "organisation__name", "short_description")
    list_filter = ("region", "category", "is_available", "is_featured")
    list_select_related = ("organisation",)

