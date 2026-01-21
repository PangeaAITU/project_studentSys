from django.urls import path
from . import views
from .views import grade_list

urlpatterns = [
    path('api/grades-test/', views.api_get_grades),
    path('api/grades/add/', views.api_add_grade),
    path("grades/", grade_list, name="grade_list"),
]
