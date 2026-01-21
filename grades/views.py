from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from school.models import Subject
from .models import Grade
from django.shortcuts import render
from users.decorators import role_required
import json



def api_get_grades(request):
    grades = Grade.objects.all()

    data = []
    for g in grades:
        data.append({
            'student': g.student.username,
            'subject': g.subject.name,
            'value': g.value
        })

    return JsonResponse(data, safe=False)



@csrf_exempt
def api_add_grade(request):
    if request.method == 'POST':
        print("API ADD GRADE CALLED")

        body = json.loads(request.body)

        student = User.objects.get(username=body['student'])
        subject = Subject.objects.get(name=body['subject'])
        value = body['value']

        Grade.objects.create(
            student=student,
            subject=subject,
            value=value
        )

        return JsonResponse({'status': 'grade added'})

    return JsonResponse({'error': 'Only POST method is allowed'})



@role_required(["student", "teacher", "admin"])
def grade_list(request):
    grades = Grade.objects.select_related("student", "subject").order_by("-created_at")
    return render(request, "grades/grade_list.html", {"grades": grades})