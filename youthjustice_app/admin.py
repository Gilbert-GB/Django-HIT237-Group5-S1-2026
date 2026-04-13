from django.contrib import admin
from .models import Program, CrimeData, EngagementData

# Models are being registered here


class OrganisationProfileAdmin(admin.ModelAdmin):
    list_display = ("organisation_name", "contact_email", "region", "user")
    search_fields = ("organisation_name", "contact_email", "user__username")
    list_filter = ("region",)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "category", "is_available")
    list_filter = ("region", "category")
    search_fields = ("name", "organisation")

admin.site.register(Program, ProgramAdmin)


class CrimeDataAdmin(admin.ModelAdmin):
    list_display = ("region", "offence_category", "year", "month", "count")
    list_filter = ("region", "year", "offence_category")
    search_fields = ("offence_category", "offence_type", "region")

admin.site.register(CrimeData, CrimeDataAdmin)


class EngagementDataAdmin(admin.ModelAdmin):
    list_display = ("year", "sex", "indigenous_status", "value_nt", "value_national")
    list_filter = ("year", "sex", "indigenous_status")

admin.site.register(EngagementData, EngagementDataAdmin)
