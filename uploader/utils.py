from django.contrib.auth.hashers import check_password

from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from datetime import timedelta
from .models import Attendance, AcademicCalendar, StudentMarks


hashed = make_password("mypassword123")
def get_student_attendance_summary(student_id):
    total_working_days = AcademicCalendar.objects.filter(
        is_working_day=True
    ).count()

    present_days = Attendance.objects.filter(
        Student_pen=student_id,
        status='P'
    ).count()

    absent_days = total_working_days - present_days

    return total_working_days, present_days, absent_days

def get_longest_attendance_streak(student_id):
    records = Attendance.objects.filter(
        Student_pen=student_id,
        status='P'
    ).order_by('attendance_date')

    longest = current = 0
    prev_date = None

    for r in records:
        if prev_date and r.attendance_date == prev_date + timedelta(days=1):
            current += 1
        else:
            current = 1
        longest = max(longest, current)
        prev_date = r.attendance_date

    return longest

def get_student_marks_summary(student_id):
    qs = StudentMarks.objects.filter(student_id=student_id)

    summary = qs.aggregate(
        total_marks=Sum('max_marks'),
        obtained_marks=Sum('marks')
    )

    # subject_wise = StudentMarks.objects.filter(
    #     student_id=student_id
    # ).values('subject', 'marks')

    subject_wise = qs.values('subject', 'marks')

    return summary, list(subject_wise)

    # return summary, subject_wise
