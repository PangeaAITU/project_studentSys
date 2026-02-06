from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subject


@login_required
def subject_list(request):
    subjects = Subject.objects.all().order_by("name")
    return render(request, "school/subject_list.html", {"subjects": subjects})
