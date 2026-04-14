from django.contrib import admin
from django.urls import path
from youthjustice_app import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ HTML PAGE
    path("dashboard/", views.dashboard_page, name="dashboard"),

    # ✅ API ENDPOINT
    path("api/dashboard/", views.dashboard_data, name="dashboard_data"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("", views.home, name="home"),
    path("programs/", views.programs, name="programs"),
    path("program/<int:program_id>/", views.program_detail, name="program_detail"),
    path("about/", views.about, name="about"),
]