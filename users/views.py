from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from grades.models import Grade
from django.db.models import Avg
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .decorators import role_required
from django.core.exceptions import PermissionDenied

@role_required(["teacher", "admin"])
def student_list(request):
    search = request.GET.get("search", "")

    students = User.objects.filter(profile__role="student")

    if search:
        students = students.filter(username__icontains=search)

    students = students.annotate(grades_count=Count("grades")).order_by("username")

    paginator = Paginator(students, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/student_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )

def student_profile(request, user_id):
    student = get_object_or_404(User, id=user_id)

    # Если студент — разрешаем смотреть только себя
    if request.user.profile.role == "student":
        if request.user.id != student.id:
            raise PermissionDenied

    grades = Grade.objects.filter(student=student).select_related("subject")
    avg_grade = grades.aggregate(avg=Avg("value"))["avg"]

    return render(
        request,
        "users/student_profile.html",
        {
            "student": student,
            "grades": grades,
            "avg_grade": round(avg_grade, 2) if avg_grade else None,
        },
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})
