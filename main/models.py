from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    teacher = models.CharField(max_length=100, verbose_name="Teacher Name")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"

        verbose_name_plural = "Courses"