from django.db import models
from django.urls import reverse


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва курсу")
    description = models.TextField(verbose_name="Опис курсу")
    teacher = models.CharField(max_length=150, verbose_name="Ім'я викладача")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("more-book", args=[str(self.id)])

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"


class Material(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Course",
    )
    title = models.CharField(max_length=200, verbose_name="Назва матеріалу")
    file = models.FileField(upload_to="materials/", verbose_name="Файл матеріалу")
    description = models.TextField(blank=True, verbose_name="Опис матеріалу")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"


class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Course",
    )
    title = models.CharField(max_length=200, verbose_name="Назва завдання")
    description = models.TextField(verbose_name="Опис завдання")
    deadline = models.DateTimeField(verbose_name="Термін виконання")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="Assignment",
    )
    student = models.CharField(max_length=150, verbose_name="Ім'я студента")
    file = models.FileField(upload_to="submissions/", verbose_name="Файл здачі")
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Оцінка"
    )

    def __str__(self):
        return self.student

    class Meta:
        verbose_name = "Здача"
        verbose_name_plural = "Здачі"
