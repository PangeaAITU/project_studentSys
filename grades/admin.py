from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """Admin interface for Grade model."""
    list_display = ('student', 'subject', 'value', 'get_letter_grade', 'teacher', 'is_active', 'created_at')
    list_filter = ('subject', 'is_active', 'created_at', 'value')
    search_fields = (
        'student__username', 
        'student__first_name', 
        'student__last_name',
        'subject__name',
        'comment'
    )
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['student', 'teacher']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Grade Information', {
            'fields': ('student', 'subject', 'value', 'teacher')
        }),
        ('Additional Details', {
            'fields': ('comment',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_letter_grade(self, obj):
        """Display letter grade."""
        return obj.get_letter_grade()
    get_letter_grade.short_description = 'Letter Grade'
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by/updated_by on save."""
        if not change:  # Creating new object
            if not obj.teacher:
                obj.teacher = request.user
        super().save_model(request, obj, form, change)