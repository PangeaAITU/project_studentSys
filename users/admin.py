from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Inline admin for Profile model."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('role', 'classroom', 'avatar', 'phone', 'address', 'date_of_birth', 'is_active')


class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with Profile inline."""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_role(self, obj):
        """Get user role from profile."""
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return 'No Profile'
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'


# Unregister the default User admin
admin.site.unregister(User)

# Register the enhanced User admin
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile model."""
    list_display = ('user', 'role', 'classroom', 'phone', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'classroom')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('School Information', {
            'fields': ('classroom',)
        }),
        ('Personal Information', {
            'fields': ('avatar', 'phone', 'address', 'date_of_birth')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )