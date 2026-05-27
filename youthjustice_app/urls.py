from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("programs/", views.programs, name="programs"),
    path("compare/", views.compare_programs, name="compare_programs"),
    path("programs/<int:pk>/", views.program_detail, name="program_detail"),
    path("requests/", views.requests_page, name="requests"),
    
    # Dashboard
    path("dashboard/", views.dashboard_page, name="dashboard"),
    path("api/dashboard/", views.dashboard_data, name="dashboard_data"),

    # Separate CRUD / management pages
    path("manage/programs/", views.ProgramManageListView.as_view(), name="manage_programs"),
    path("manage/programs/add/", views.ProgramCreateView.as_view(), name="add_program"),
    path("manage/programs/<int:pk>/edit/", views.ProgramUpdateView.as_view(), name="edit_program"),
    path("manage/programs/<int:pk>/delete/", views.ProgramDeleteView.as_view(), name="delete_program"),

    # Engagement dashboard
    path("engagement/", views.engagement_page, name="engagement"),
    path("api/engagement/", views.engagement_data, name="engagement_data"),

    # Organisations
    path("organisations/", views.organisation_list, name="organisations"),
    path("organisations/<int:pk>/", views.organisation_detail, name="organisation_detail"),

    # CSV exports
    path("export/programs/", views.export_programs_csv, name="export_programs"),
    path("export/crime/", views.export_crime_csv, name="export_crime"),
    path("export/engagement/", views.export_engagement_csv, name="export_engagement"),

    # Region profile
    path("region/<str:region_slug>/", views.region_profile, name="region_profile"),
]

