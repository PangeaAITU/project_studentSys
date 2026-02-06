from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


def validate_avatar_size(file):
    """Validate that avatar file size doesn't exceed 2MB."""
    max_size = 2 * 1024 * 1024  # 2 MB
    if file.size > max_size:
        raise ValidationError(f'File size must not exceed 2MB. Current size: {file.size / 1024 / 1024:.2f}MB')


class Profile(models.Model):
    """User profile with role-based access control."""
    
    ROLE_CHOICES = (
        ("admin", "Administrator"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default="student",
        db_index=True
    )
    
    classroom = models.ForeignKey(
        "school.ClassRoom", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="students"
    )
    
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
            validate_avatar_size
        ]
    )
    
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Audit fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username']
        indexes = [
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['classroom']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    
    def is_student(self):
        """Check if profile belongs to a student."""
        return self.role == 'student'
    
    def is_teacher(self):
        """Check if profile belongs to a teacher."""
        return self.role == 'teacher'
    
    def is_admin(self):
        """Check if profile belongs to an admin."""
        return self.role == 'admin'
    
    def clean(self):
        """Validate model data before saving."""
        super().clean()
        
        # Teachers and admins should not have classrooms
        if self.role in ['teacher', 'admin'] and self.classroom:
            raise ValidationError({
                'classroom': f'{self.get_role_display()}s should not be assigned to classrooms.'
            })


@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    """Automatically create or update user profile when User is saved."""
    try:
        if created:
            Profile.objects.create(user=instance)
            logger.info(f"Profile created for user: {instance.username}")
        else:
            if hasattr(instance, 'profile'):
                instance.profile.save()
    except Exception as e:
        logger.error(f"Error managing profile for user {instance.username}: {str(e)}")
        raise