from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value')
    search_fields = ('student__username',)
    list_filter = ('subject', 'value')
