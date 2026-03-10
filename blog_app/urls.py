from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.post_details, name='post_details'),
]
