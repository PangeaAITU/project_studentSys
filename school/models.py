from django.db import models


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)  
    year = models.IntegerField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
