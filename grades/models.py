from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from school.models import Subject
import logging

logger = logging.getLogger(__name__)


class Grade(models.Model):
    """Student grade/mark for a specific subject."""
    
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="grades",
        limit_choices_to={'profile__role': 'student'}
    )
    
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE,
        related_name="grades"
    )
    
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_grades",
        limit_choices_to={'profile__role': 'teacher'}
    )
    
    value = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0, message="Grade cannot be negative"),
            MaxValueValidator(100, message="Grade cannot exceed 100")
        ]
    )
    
    comment = models.TextField(blank=True)
    
    # Audit trail
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'subject']),
            models.Index(fields=['subject', 'created_at']),
            models.Index(fields=['student', 'is_active']),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}: {self.value}"
    
    def get_letter_grade(self):
        """Convert numerical grade to letter grade."""
        if self.value >= 90:
            return 'A'
        elif self.value >= 80:
            return 'B'
        elif self.value >= 70:
            return 'C'
        elif self.value >= 60:
            return 'D'
        else:
            return 'F'
    
    def is_passing(self):
        """Check if grade is passing (>= 60)."""
        return self.value >= 60
    
    def clean(self):
        """Validate model data before saving."""
        super().clean()
        
        # Verify student has the correct role
        if self.student and hasattr(self.student, 'profile'):
            if self.student.profile.role != 'student':
                raise ValidationError({
                    'student': 'Selected user is not a student.'
                })
        
        # Verify teacher has the correct role if provided
        if self.teacher and hasattr(self.teacher, 'profile'):
            if self.teacher.profile.role != 'teacher':
                raise ValidationError({
                    'teacher': 'Selected user is not a teacher.'
                })
    
    def save(self, *args, **kwargs):
        """Override save to run validation."""
        self.full_clean()
        
        if self.pk:
            logger.info(f"Grade updated: {self}")
        else:
            logger.info(f"Grade created: {self}")
        
        super().save(*args, **kwargs)