from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, "home.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("school/", include("school.urls")),
    path("grades/", include("grades.urls")),
    path("users/", include("users.urls")),
]
