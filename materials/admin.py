from django.contrib import admin
from materials.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "owner")

    ordering = ('-id',)