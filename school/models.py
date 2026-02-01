from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()

    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="classes"
    )

    subjects = models.ManyToManyField(
        "Subject",
        blank=True,
        related_name="classes"
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
