from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('profile/', views.student_profile),
]
