from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Subject(models.Model):
    """Academic subject taught in the school."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    """Classroom/Class group in the school."""
    
    name = models.CharField(max_length=50, unique=True)
    year = models.IntegerField()
    
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes",
        limit_choices_to={'profile__role': 'teacher'}
    )
    
    subjects = models.ManyToManyField(
        Subject,
        blank=True,
        related_name="classes"
    )
    
    max_students = models.PositiveSmallIntegerField(default=30)
    room_number = models.CharField(max_length=20, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year', 'name']
        indexes = [
            models.Index(fields=['year', 'is_active']),
            models.Index(fields=['teacher']),
        ]

    def __str__(self):
        return f"{self.name} ({self.year})"
    
    def get_student_count(self):
        """Get current number of students in classroom."""
        return self.students.filter(is_active=True).count()
    
    def is_full(self):
        """Check if classroom has reached maximum capacity."""
        return self.get_student_count() >= self.max_students
    
    def get_available_seats(self):
        """Get number of available seats."""
        return max(0, self.max_students - self.get_student_count())
    
    def clean(self):
        """Validate model data before saving."""
        super().clean()
        
        # Validate teacher role
        if self.teacher and hasattr(self.teacher, 'profile'):
            if self.teacher.profile.role != 'teacher':
                raise ValidationError({
                    'teacher': 'Selected user is not a teacher.'
                })
        
        # Validate year
        current_year = timezone.now().year
        if self.year < 2000 or self.year > current_year + 1:
            raise ValidationError({
                'year': f'Year must be between 2000 and {current_year + 1}.'
            })
        
        # Check student capacity
        if self.pk and self.get_student_count() > self.max_students:
            raise ValidationError({
                'max_students': f'Cannot set max students below current enrollment ({self.get_student_count()}).'
            })
    
    def save(self, *args, **kwargs):
        """Override save to run validation."""
        self.full_clean()
        logger.info(f"Classroom {'updated' if self.pk else 'created'}: {self.name}")
        super().save(*args, **kwargs)