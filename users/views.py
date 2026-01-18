from django.shortcuts import render
from grades.models import Grade


def student_profile(request):
    grades = Grade.objects.filter(student=request.user)
    return render(request, 'users/student_profile.html', {
        'grades': grades
    })