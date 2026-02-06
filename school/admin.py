from django.contrib import admin
from .models import Subject, ClassRoom


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin interface for Subject model."""
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Subject Information', {
            'fields': ('name', 'description')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    """Admin interface for ClassRoom model."""
    list_display = ('name', 'year', 'teacher', 'get_student_count', 'max_students', 'is_full', 'is_active')
    list_filter = ('year', 'is_active', 'teacher')
    search_fields = ('name', 'room_number', 'teacher__username')
    filter_horizontal = ('subjects',)
    readonly_fields = ('created_at', 'updated_at', 'get_student_count', 'get_available_seats')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'year', 'room_number')
        }),
        ('Assignment', {
            'fields': ('teacher', 'subjects')
        }),
        ('Capacity', {
            'fields': ('max_students', 'get_student_count', 'get_available_seats')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_student_count(self, obj):
        """Display student count."""
        return obj.get_student_count()
    get_student_count.short_description = 'Students'
    
    def is_full(self, obj):
        """Display if classroom is full."""
        return obj.is_full()
    is_full.boolean = True
    is_full.short_description = 'Full?'
    
    def get_available_seats(self, obj):
        """Display available seats."""
        return obj.get_available_seats()
    get_available_seats.short_description = 'Available Seats'