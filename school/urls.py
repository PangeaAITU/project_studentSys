from django.urls import path
from . import views
from .views import subject_list

urlpatterns = [
    path("subjects/", subject_list, name="subject_list"),
]
