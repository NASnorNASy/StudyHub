from django.contrib import admin
from .models import Course, Material, Assignment, Submission


admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Assignment)
admin.site.register(Submission)
