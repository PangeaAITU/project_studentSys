from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from users.api import StudentViewSet
from grades.api import GradeViewSet
from school.api import ClassRoomViewSet


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return render(request, "landing.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("school/", include("school.urls")),
    path("grades/", include("grades.urls")),
    path("users/", include("users.urls")),
]

router = DefaultRouter()
router.register(r"api/students", StudentViewSet)
router.register(r"api/grades", GradeViewSet)
router.register(r"api/classes", ClassRoomViewSet)


urlpatterns += router.urls

