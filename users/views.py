from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from grades.models import Grade
from .decorators import role_required
import logging

logger = logging.getLogger(__name__)


@login_required
@role_required(["teacher", "admin"])
def student_list(request):
    """List all students with search and pagination."""
    search = request.GET.get("search", "")
    
    # Optimize query with select_related and prefetch_related
    students = User.objects.filter(
        profile__role="student",
        profile__is_active=True
    ).select_related('profile', 'profile__classroom')
    
    if search:
        students = students.filter(
            username__icontains=search
        ) | students.filter(
            first_name__icontains=search
        ) | students.filter(
            last_name__icontains=search
        )
    
    students = students.annotate(
        grades_count=Count("grades")
    ).order_by("username")
    
    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    logger.info(f"Student list viewed by {request.user.username}, search: '{search}'")
    
    return render(
        request,
        "users/student_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )


@login_required
def student_profile(request, user_id):
    """Display student profile with grades."""
    student = get_object_or_404(
        User.objects.select_related('profile', 'profile__classroom'),
        id=user_id
    )
    
    # Check permissions
    if hasattr(request.user, 'profile'):
        if request.user.profile.role == "student":
            if request.user.id != student.id:
                logger.warning(f"Student {request.user.username} tried to access profile of {student.username}")
                raise PermissionDenied("You can only view your own profile.")
    
    # Optimize grades query
    grades = Grade.objects.filter(
        student=student,
        is_active=True
    ).select_related("subject", "teacher").order_by('-created_at')
    
    # Calculate average grade
    avg_grade = grades.aggregate(avg=Avg("value"))["avg"]
    
    # Calculate subject-wise averages
    subject_averages = {}
    for grade in grades:
        subject_name = grade.subject.name
        if subject_name not in subject_averages:
            subject_averages[subject_name] = []
        subject_averages[subject_name].append(grade.value)
    
    subject_averages = {
        subject: round(sum(values) / len(values), 2)
        for subject, values in subject_averages.items()
    }
    
    logger.info(f"Profile viewed: {student.username} by {request.user.username}")
    
    return render(
        request,
        "users/student_profile.html",
        {
            "student": student,
            "grades": grades,
            "avg_grade": round(avg_grade, 2) if avg_grade else None,
            "subject_averages": subject_averages,
        },
    )


def register(request):
    """User registration view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"New user registered: {user.username}")
            return redirect("login")
    else:
        form = UserCreationForm()
    
    return render(request, "users/register.html", {"form": form})