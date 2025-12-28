from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
