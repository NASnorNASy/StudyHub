from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("home-student/", views.home_student, name="home-student"),
    path("all-courses-student/", views.all_courses_student, name="all-courses-student"),
    path("materials-student/", views.materials_student, name="materials-student"),
    path("assignments-student/", views.assignments_student, name="assignments-student"),
    path("my-works-student/", views.my_works_student, name="my-works-student"),
    path("home-teacher/", views.home_teacher, name="home-teacher"),
    path("materials-teacher/", views.materials_teacher, name="materials-teacher"),
    path("assignments-teacher/", views.assignments_teacher, name="assignments-teacher"),
    path(
        "students-works-teacher/",
        views.students_works_teacher,
        name="students-works-teacher",
    ),
    path("home-admin/", views.home_admin, name="home-admin"),
    path("create-course-admin/", views.create_course_admin, name="create-course-admin"),
    path(
        "view-course-admin/<int:course_id>/",
        views.view_course_admin,
        name="view-course-admin",
    ),
    path(
        "edit-course-admin/<int:course_id>/",
        views.edit_course_admin,
        name="edit-course-admin",
    ),
    path(
        "delete-course-admin/<int:course_id>/",
        views.delete_course_admin,
        name="delete-course-admin",
    ),
    path("users-admin/", views.users_admin, name="users-admin"),
    path(
        "edit-user-role-admin/<str:user_id>/",
        views.edit_user_role_admin,
        name="edit-user-role-admin",
    ),
    path(
        "delete-user-admin/<str:user_id>/",
        views.delete_user_admin,
        name="delete-user-admin",
    ),
]
