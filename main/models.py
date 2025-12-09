from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    teacher = models.CharField(max_length=150, verbose_name="Teacher Name")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Material(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Course",
    )
    title = models.CharField(max_length=200, verbose_name="Material Title")
    file = models.FileField(upload_to="materials/", verbose_name="Material File")
    description = models.TextField(blank=True, verbose_name="Material Description")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"


class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Course",
    )
    title = models.CharField(max_length=200, verbose_name="Assignment Title")
    description = models.TextField(verbose_name="Assignment Description")
    deadline = models.DateTimeField(verbose_name="Deadline")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="Assignment",
    )
    student = models.CharField(max_length=150, verbose_name="Student Name")
    file = models.FileField(upload_to="submissions/", verbose_name="Submission File")
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Grade"
    )

    def __str__(self):
        return self.student

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
