from django.contrib import admin
from .models import ClassRoom, Subject


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ('name',)
    list_filter = ('teacher',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom')
    search_fields = ('name',)
    list_filter = ('classroom',)
