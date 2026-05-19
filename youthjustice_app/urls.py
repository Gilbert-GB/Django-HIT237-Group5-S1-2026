from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("programs/", views.programs, name="programs"),
    path("programs/<int:pk>/", views.program_detail, name="program_detail"),

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
]
