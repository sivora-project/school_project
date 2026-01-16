from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Student,
    Classes,
    Attendance,
    AcademicCalendar,
    StudentMarks
)

admin.site.register(Student)
admin.site.register(Classes)
admin.site.register(Attendance)
admin.site.register(AcademicCalendar)
admin.site.register(StudentMarks)

