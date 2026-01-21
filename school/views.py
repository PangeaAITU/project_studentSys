from django.shortcuts import render
from .models import Subject


def subject_list(request):
    subjects = Subject.objects.all().order_by("name")
    return render(request, "school/subject_list.html", {"subjects": subjects})
