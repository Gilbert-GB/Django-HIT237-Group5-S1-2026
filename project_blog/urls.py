from django.contrib import admin
from django.urls import path
from youthjustice_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("program/<int:program_id>/", views.program_detail, name="program_detail"),
    path("about/", views.about, name="about"),
]