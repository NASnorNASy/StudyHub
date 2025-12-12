from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.custom_login_view, name="login"),
    path("home-student/", views.home_student, name="home-student"),
    path("all-courses-student/", views.all_courses_student, name="all-courses-student"),
    path("materials-student/", views.materials_student, name="materials-student"),
    path("assignments-student/", views.assignments_student, name="assignments-student"),
    path("my-works-student/", views.my_works_student, name="my-works-student"),
     path("home-teacher/", views.home_teacher, name="home-teacher"),
]
