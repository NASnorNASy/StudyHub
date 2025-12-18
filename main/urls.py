from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("home-student/", views.home_student, name="home-student"),
    path(
        "course-view-student/<int:course_id>/",
        views.course_view_student,
        name="course-view-student",
    ),
    path("join-course/<int:course_id>/", views.join_course, name="join-course"),
    path("all-courses-student/", views.all_courses_student, name="all-courses-student"),
    path("materials-student/", views.materials_student, name="materials-student"),
    path(
        "comments-student/<int:material_id>/",
        views.comments_student,
        name="comments-student",
    ),
    path("assignments-student/", views.assignments_student, name="assignments-student"),
    path(
        "assignments-student-view/<int:assignment_id>/",
        views.assignments_student_view,
        name="assignments-student-view",
    ),
    path("my-works-student/", views.my_works_student, name="my-works-student"),
    path("home-teacher/", views.home_teacher, name="home-teacher"),
    path(
        "create-course-teacher/",
        views.create_course_teacher,
        name="create-course-teacher",
    ),
    path("materials-teacher/", views.materials_teacher, name="materials-teacher"),
    path(
        "create-materials-teacher/",
        views.create_materials_teacher,
        name="create-materials-teacher",
    ),
    path(
        "comments-teacher/<int:material_id>/",
        views.comments_teacher,
        name="comments-teacher",
    ),
    path("assignments-teacher/", views.assignments_teacher, name="assignments-teacher"),
    path(
        "create-assignments-teacher/",
        views.create_assignments_teacher,
        name="create-assignments-teacher",
    ),
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
        "delete-materials-admin/<int:material_id>/",
        views.delete_materials_admin,
        name="delete-materials-admin",
    ),
    path(
        "delete-assignments-admin/<int:assignment_id>/",
        views.delete_assignments_admin,
        name="delete-assignments-admin",
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
