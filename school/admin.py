from django.contrib import admin
from .models import ClassRoom, Subject


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year")
    search_fields = ("name",)
    list_filter = ("year",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
