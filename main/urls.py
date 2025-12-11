from django.urls import path
from . import views


urlpatterns = [
    path("", views.login, name="login"),
    path("home-student/", views.home_student, name="home-student"),
]
