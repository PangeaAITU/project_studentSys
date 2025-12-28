from django.db import models
from django.contrib.auth.models import User
from school.models import Subject


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)
