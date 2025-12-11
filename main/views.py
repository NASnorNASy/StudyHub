from django.shortcuts import render
from .models import Course, Material, Assignment, Submission


def login(request):

    return render(request, "login.html")


def home_student(request):

    return render(request, "home_student.html")
