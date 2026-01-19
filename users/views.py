from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from grades.models import Grade


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/users/profile/')

    err = ''

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('/users/profile/')
        else:
            err = 'Wrong username or password'

    return render(request, 'users/login.html', {'err': err})


def user_logout(request):
    logout(request)
    return redirect('/users/login/')


def student_profile(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')

    grades = Grade.objects.filter(student=request.user)
    return render(request, 'users/student_profile.html', {'grades': grades})
