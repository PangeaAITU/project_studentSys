from django.db import models
from django.contrib.auth.models import User
from school.models import Subject


class Grade(models.Model):
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="grades"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="given_grades"
    )

    value = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "subject", "created_at")

    def __str__(self):
        return f"{self.student.username} - {self.subject} = {self.value}"
