from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Material, Assignment, Submission, Comment
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg


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
    error_email = ""
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
            error_email = "Користувач з таким email вже існує."
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
            "error_email": error_email,
            "error_password": error_password,
        },
    )


def is_student(user):
    return user.groups.filter(name="Студент").exists()


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def home_student(request):
    courses = request.user.courses.all()
    return render(request, "home_student.html", {"courses": courses})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def course_view_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    assignments = Assignment.objects.filter(course=course).order_by("deadline")
    total_tasks = assignments.count()

    submissions = Submission.objects.filter(
        student=request.user, assignment__course=course
    ).select_related("assignment")

    submitted_tasks = submissions.count()
    graded_tasks = submissions.filter(grade__isnull=False).count()

    progress_percent = 0
    if total_tasks > 0:
        progress_percent = int((submitted_tasks / total_tasks) * 100)

    graded_submissions = submissions.filter(grade__isnull=False)
    average_grade = graded_submissions.aggregate(avg=Avg("grade"))["avg"] or 0

    assignment_data = []
    for assignment in assignments:
        submission = submissions.filter(assignment=assignment).first()
        assignment_data.append(
            {
                "assignment": assignment,
                "submission": submission,
                "is_submitted": submission is not None,
                "is_graded": submission.grade is not None if submission else False,
                "grade": submission.grade if submission else None,
            }
        )

    context = {
        "course": course,
        "progress_percent": progress_percent,
        "submitted_tasks": submitted_tasks,
        "graded_tasks": graded_tasks,
        "total_tasks": total_tasks,
        "average_grade": round(average_grade, 1),
        "assignment_data": assignment_data,
    }

    return render(request, "course_view_student.html", context)


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    course.students.add(request.user)

    return redirect("home-student")


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def all_courses_student(request):
    courses = Course.objects.all()

    paginator = Paginator(courses, 6)
    page_number = request.GET.get("page")

    try:
        paged_courses = paginator.page(page_number)
    except PageNotAnInteger:
        paged_courses = paginator.page(1)
    except EmptyPage:
        paged_courses = paginator.page(paginator.num_pages)

    return render(request, "all_courses_student.html", {"courses": paged_courses})


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def materials_student(request):
    materials_student = Material.objects.filter(
        course__students=request.user
    ).select_related("course")

    search_materials = request.GET.get("search", "").strip().lower()
    if search_materials:
        materials_student = list(materials_student)
        materials_student = [
            material
            for material in materials_student
            if search_materials in material.title.lower()
        ]

    return render(
        request, "materials_student.html", {"materials_student": materials_student}
    )


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def comments_student(request, material_id):
    material = Material.objects.get(id=material_id)
    comments = material.comments.all()

    if request.method == "POST":
        Comment.objects.create(
            material=material, author=request.user, text=request.POST["text"]
        )
        return redirect(request.path)

    return render(
        request, "comments_student.html", {"material": material, "comments": comments}
    )


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def assignments_student(request):
    user = request.user

    all_assignments = Assignment.objects.filter(
        course__students=request.user
    ).select_related("course")

    assignments_list = []

    for assignment in all_assignments:
        has_submitted = Submission.objects.filter(
            assignment=assignment, student=user
        ).exists()

        assignments_list.append(
            {
                "assignment": assignment,
                "has_submitted": has_submitted,
            }
        )

    return render(
        request,
        "assignments_student.html",
        {
            "assignments_student_list": assignments_list,
        },
    )


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def assignments_student_view(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    user = request.user

    existing_submission = Submission.objects.filter(
        assignment=assignment, student=user
    ).first()

    if request.method == "POST":
        if not existing_submission:
            uploaded_file = request.FILES.get("file")
            if uploaded_file:
                Submission.objects.create(
                    assignment=assignment, student=user, file=uploaded_file
                )
                return redirect("assignments-student")
            else:
                pass

    context = {
        "assignment": assignment,
        "submission": existing_submission,
    }
    return render(request, "assignments_student_view.html", context)


@login_required(login_url="login")
@user_passes_test(is_student, login_url="login")
def my_works_student(request):
    user = request.user

    all_assignments = Assignment.objects.filter(
        course__students=request.user
    ).select_related("course")

    assignments_list = []

    for assignment in all_assignments:
        submission_obj = None
        score = None
        has_submitted = False

        try:
            submission_obj = Submission.objects.get(assignment=assignment, student=user)
            has_submitted = True
            score = submission_obj.grade
        except Submission.DoesNotExist:
            pass

        assignments_list.append(
            {
                "assignment": assignment,
                "has_submitted": has_submitted,
                "score": score,
                "submission": submission_obj,
            }
        )

    return render(
        request,
        "my_works_student.html",
        {
            "assignments_student_list": assignments_list,
        },
    )


def is_teacher(user):
    return user.groups.filter(name="Викладач").exists()


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def home_teacher(request):
    courses = Course.objects.all()
    return render(request, "home_teacher.html", {"courses": courses})


@permission_required("main.add_course", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def create_course_teacher(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if not title or not description:
            error = "Всі поля повинні бути заповнені."
            return render(request, "create_course_teacher.html", {"error": error})

        Course.objects.create(
            title=title,
            description=description,
            teacher=request.user,
        )
        return redirect("home-teacher")

    return render(request, "create_course_teacher.html", {"error": error})


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def materials_teacher(request):
    materials = Material.objects.filter(course__teacher=request.user)

    search_materials_teacher = request.GET.get("searcher", "").strip().lower()
    if search_materials_teacher:
        materials = list(materials)
        materials = [
            m_t for m_t in materials if search_materials_teacher in m_t.title.lower()
        ]

    return render(request, "materials_teacher.html", {"materials": materials})


@permission_required("main.add_material", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def create_materials_teacher(request):
    error = ""
    if request.method == "POST":
        course_id = request.POST.get("course")
        course = Course.objects.get(id=course_id)
        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")

        if not course or not title or not description or not file:
            error = "Всі поля повинні бути заповнені."
            return render(request, "create_materials_teacher.html", {"error": error})

        Material.objects.create(
            course=course, title=title, description=description, file=file
        )
        return redirect("materials-teacher")

    courses = Course.objects.all()

    return render(
        request, "create_materials_teacher.html", {"courses": courses, "error": error}
    )


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def comments_teacher(request, material_id):
    material = Material.objects.get(id=material_id)
    comments = material.comments.all()

    if request.method == "POST":
        Comment.objects.create(
            material=material, author=request.user, text=request.POST["text"]
        )
        return redirect(request.path)

    return render(
        request, "comments_teacher.html", {"material": material, "comments": comments}
    )


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def assignments_teacher(request):
    assignments = Assignment.objects.all()
    return render(request, "assignments_teacher.html", {"assignments": assignments})


@permission_required("main.add_assignment", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def create_assignments_teacher(request):
    error = ""
    if request.method == "POST":
        course_id = request.POST.get("course")
        course = Course.objects.get(id=course_id)
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")

        if not course or not title or not description or not deadline:
            error = "Всі поля повинні бути заповнені."
            return render(request, "create_assignments_teacher.html", {"error": error})

        Assignment.objects.create(
            course=course, title=title, description=description, deadline=deadline
        )
        return redirect("assignments-teacher")

    courses = Course.objects.all()

    return render(
        request, "create_assignments_teacher.html", {"courses": courses, "error": error}
    )


@login_required(login_url="login")
@user_passes_test(is_teacher, login_url="login")
def students_works_teacher(request):
    error_data = {"message": "", "submission_id": None}

    if request.method == "POST":
        submission_id = request.POST.get("submission_id")
        new_grade_str = request.POST.get("grade", "").strip()

        if submission_id and new_grade_str:
            submission = get_object_or_404(Submission, id=submission_id)

            try:
                new_grade = int(new_grade_str)
            except ValueError:
                error_data["message"] = "Оцінка повинна бути числом."
                error_data["submission_id"] = submission_id
            else:
                if not (0 <= new_grade <= 100):
                    error_data["message"] = (
                        "Оцінка повинна бути в діапазоні від 0 до 100."
                    )
                    error_data["submission_id"] = submission_id
                else:
                    submission.grade = new_grade
                    submission.save()

    submissions = (
        Submission.objects.filter(assignment__course__teacher=request.user)
        .select_related("assignment", "student", "assignment__course")
        .order_by("-assignment__deadline")
    )

    return render(
        request,
        "students_works_teacher.html",
        {"submissions": submissions, "error_data": error_data},
    )


def is_admin(user):
    return user.groups.filter(name="Адмін").exists()


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def home_admin(request):
    courses = Course.objects.all()
    return render(request, "home_admin.html", {"courses": courses})


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def users_admin(request):
    users = User.objects.all()
    return render(request, "users_admin.html", {"users": users})


@permission_required("auth.change_user", login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def edit_user_role_admin(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        new_role = request.POST.get("role")
        user.groups.clear()
        if new_role == "Студент":
            group = Group.objects.get(name="Студент")
        elif new_role == "Викладач":
            group = Group.objects.get(name="Викладач")
        elif new_role == "Адмін":
            group = Group.objects.get(name="Адмін")
        else:
            group = None

        if group:
            user.groups.add(group)

        return redirect("users-admin")

    return render(request, "edit_user_role_admin.html", {"user": user})


@permission_required("auth.delete_user", login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def delete_user_admin(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect("users-admin")
    return render(request, "delete_user_admin.html", {"user": user})


@permission_required("main.add_course", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def create_course_admin(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        teacher_id = request.POST.get("teacher")
        teacher = User.objects.get(id=teacher_id)

        Course.objects.create(
            title=title,
            description=description,
            teacher=teacher,
        )

        if not title or not description or not teacher:
            error = "Всі поля повинні бути заповнені."

        return redirect("home-admin")

    teachers = User.objects.filter(groups__name="Викладач")
    return render(
        request, "create_course_admin.html", {"teachers": teachers, "error": error}
    )


@permission_required("main.view_course", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def view_course_admin(request, course_id):
    course = Course.objects.get(id=course_id)

    materials = Material.objects.filter(course=course)
    assignments = Assignment.objects.filter(course=course)

    return render(
        request,
        "view_course_admin.html",
        {"course": course, "materials": materials, "assignments": assignments},
    )


@permission_required("main.delete_material", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def delete_materials_admin(request, material_id):
    material = Material.objects.get(id=material_id)
    if request.method == "POST":
        material.delete()
        return redirect("home-admin")

    return render(
        request,
        "delete_materials_admin.html",
        {"material": material},
    )


@permission_required("main.delete_assignment", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def delete_assignments_admin(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == "POST":
        assignment.delete()
        return redirect("home-admin")

    return render(
        request,
        "delete_assignments_admin.html",
        {"assignment": assignment},
    )


@permission_required("main.change_course", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def edit_course_admin(request, course_id):
    course = Course.objects.get(id=course_id)
    error = ""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        teacher_id = request.POST.get("teacher")
        teacher = User.objects.get(id=teacher_id)

        if not title or not description or not teacher:
            error = "Всі поля повинні бути заповнені."
        else:
            course.title = title
            course.description = description
            course.teacher = teacher
            course.save()
            return redirect("home-admin")

    teachers = User.objects.filter(groups__name="Викладач")
    return render(
        request,
        "edit_course_admin.html",
        {"course": course, "teachers": teachers, "error": error},
    )


@permission_required("main.delete_course", raise_exception=True, login_url="login")
@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def delete_course_admin(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect("home-admin")
    return render(request, "delete_course_admin.html", {"course": course})
