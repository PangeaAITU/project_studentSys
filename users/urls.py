from django.urls import path
from . import views
from .views import student_list
from .views import student_profile
from .views import register
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("students/", student_list, name="student_list"),
    path("students/<int:user_id>/", student_profile, name="student_profile"),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
