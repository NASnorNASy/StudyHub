from django.shortcuts import render, redirect
from .models import Course, Material, Assignment, Submission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def check_student(user):
    return user.groups.filter(name="Студент").exists()


def check_teacher(user):
    return user.groups.filter(name="Викладач").exists()

def check_admin(user):
    return user.groups.filter(name="Адмін").exists()


@login_required
def dashboard(request):
    user = request.user

    if user.groups.filter(name="Студент").exists():
        return redirect("home-student")
    elif user.groups.filter(name="Викладач").exists():
        return redirect("home-teacher")
    elif user.groups.filter(name="Адмін").exists():
        return redirect("home-admin")
    else:
        return render(request, "login.html")


def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_group(request.user)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect_based_on_group(user)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def redirect_based_on_group(user):
    """Redirect user based on their group membership"""
    if user.groups.filter(name='Студент').exists():
        return redirect('home-student')
    elif user.groups.filter(name='Викладач').exists():
        return redirect('home-teacher')
    elif user.groups.filter(name='Адмін').exists():
        return redirect('home-admin')
    else:
        return redirect('login')


# ---------------------------------------------------------Student


@login_required(login_url="login")
def home_student(request):
    return render(request, "home_student.html")


def all_courses_student(request):
    return render(request, "all_courses_student.html")


def materials_student(request):
    return render(request, "materials_student.html")


def assignments_student(request):
    return render(request, "assignments_student.html")


def my_works_student(request):
    return render(request, "my_works_student.html")


# ---------------------------------------------------------Teacher

def home_teacher(request):
    return render(request, "home_teacher.html")