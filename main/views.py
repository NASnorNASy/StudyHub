from django.shortcuts import render, redirect
from .models import Course, Material, Assignment, Submission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect_to_group(request.user)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect_to_group(user)
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def redirect_to_group(user):
    if user.groups.filter(name="Студент").exists():
        return redirect("home-student")
    elif user.groups.filter(name="Викладач").exists():
        return redirect("home-teacher")
    elif user.groups.filter(name="Адмін").exists():
        return redirect("home-admin")
    else:
        return redirect("login")


def register_view(request):
    error_user = ""
    error_emeil = ""
    error_password = ""
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            error_user = "Користувач з таким ім'ям вже існує."
        elif User.objects.filter(email=email).exists():
            error_emeil = "Користувач з таким email вже існує."
        elif password != password2:
            error_password = "Паролі не співпадають."
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )

            if role == "student":
                group = Group.objects.get(name="Студент")
            elif role == "teacher":
                group = Group.objects.get(name="Викладач")
            elif role == "admin":
                group = Group.objects.get(name="Адмін")
            else:
                group = None

            if group:
                user.groups.add(group)

            return redirect_to_group(user)

    return render(
        request,
        "register.html",
        {
            "error_user": error_user,
            "error_emeil": error_emeil,
            "error_password": error_password,
        },
    )


# ---------------------------------------------------------Student
def is_student(user):
    return user.groups.filter(name="Студент").exists()


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def home_student(request):
    return render(request, "home_student.html")


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def all_courses_student(request):
    return render(request, "all_courses_student.html")


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def materials_student(request):
    return render(request, "materials_student.html")


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def assignments_student(request):
    return render(request, "assignments_student.html")


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def my_works_student(request):
    return render(request, "my_works_student.html")


# ---------------------------------------------------------Teacher
def is_teacher(user):
    return user.groups.filter(name="Викладач").exists()


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def home_teacher(request):
    return render(request, "home_teacher.html")


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def materials_teacher(request):
    return render(request, "materials_teacher.html")


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def assignments_teacher(request):
    return render(request, "assignments_teacher.html")


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def students_works_teacher(request):
    return render(request, "students_works_teacher.html")


# ---------------------------------------------------------Admin
def is_admin(user):
    return user.groups.filter(name="Адмін").exists()


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def home_admin(request):
    return render(request, "home_admin.html")


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def users_admin(request):
    return render(request, "users_admin.html")
