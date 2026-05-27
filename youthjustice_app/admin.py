from django.contrib import admin
from .models import (
    Organisation,
    Program,
    CrimeDataSnapshot,
    CrimeData,
    EngagementData,
    HelpRequest,
    ProgramInfoReport,
)


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

# ============================================================
# CRIME DATA SNAPSHOT ADMIN
# ============================================================
@admin.register(CrimeDataSnapshot)
class CrimeDataSnapshotAdmin(admin.ModelAdmin):
    list_display = ("program", "region", "year", "total_offences", "created_at")
    search_fields = ("program__name", "region", "summary")
    list_filter = ("region", "year")
    list_select_related = ("program",)


# CRIME DATA ADMIN

@admin.register(CrimeData)
class CrimeDataAdmin(admin.ModelAdmin):
    list_display = (
        "region",
        "year",
        "month",
        "offence_category",
        "offence_type",
        "count",
    )
    search_fields = ("region", "offence_category", "offence_type")
    list_filter = ("region", "year", "month")


# ENGAGEMENT DATA ADMIN

@admin.register(EngagementData)
class EngagementDataAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "sex",
        "indigenous_status",
        "value_nt",
        "value_national",
    )
    search_fields = ("indigenous_status", "sex", "measure")
    list_filter = ("year", "sex", "indigenous_status")

    # HELP REQUEST ADMIN

@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "program",
        "status",
        "created_at",
    )
    search_fields = ("name", "email", "program__name")
    list_filter = ("status", "created_at")
    list_select_related = ("program",)


# PROGRAM INFO REPORT ADMIN

@admin.register(ProgramInfoReport)
class ProgramInfoReportAdmin(admin.ModelAdmin):
    list_display = (
        "program",
        "issue_type",
        "status",
        "created_at",
    )
    search_fields = ("program__name", "message", "email")
    list_filter = ("issue_type", "status", "created_at")
    list_select_related = ("program",)