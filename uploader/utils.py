from django.db.models import Sum
from datetime import timedelta
from collections import defaultdict

from .models import Attendance, AcademicCalendar, StudentMarks


# =========================
# EXISTING FUNCTIONS (UNCHANGED)
# =========================

def get_student_attendance_summary(student_id, month=None):
    attendance_qs = Attendance.objects.filter(Student_pen=student_id)
    calendar_qs = AcademicCalendar.objects.filter(is_working_day=True)

    if month:
        year, mon = month.split('-')
        attendance_qs = attendance_qs.filter(
            attendance_date__year=year,
            attendance_date__month=mon
        )
        calendar_qs = calendar_qs.filter(
            date__year=year,
            date__month=mon
        )

    present_days = attendance_qs.filter(status='P').count()
    total_days = calendar_qs.count()
    absent_days = total_days - present_days

    return total_days, present_days, absent_days


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

    subject_wise = qs.values(
        'exam_type',
        'subject',
        'marks',
        'max_marks'
    )

    return summary, list(subject_wise)


# =========================
# 🆕 NEW FUNCTIONS
# =========================

def get_regular_absent_students(attendance_qs):
    """
    Detect consecutive absent days per student
    Returns: {student_id: max_consecutive_absent_days}
    """
    student_dates = defaultdict(list)

    for att in attendance_qs.filter(status='A').order_by('attendance_date'):
        student_dates[att.Student_pen].append(att.attendance_date)

    result = {}

    for student_id, dates in student_dates.items():
        max_streak = current = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 1

        if max_streak >= 2:
            result[student_id] = max_streak

    return result


def get_monthly_attendance_trend(attendance_qs):
    """
    Returns:
    labels -> [1,2,3,...]
    data   -> [attendance_percentage]
    """
    monthly = defaultdict(lambda: {'total': 0, 'present': 0})

    for att in attendance_qs:
        m = att.attendance_date.month
        monthly[m]['total'] += 1
        if att.status == 'P':
            monthly[m]['present'] += 1

    labels = []
    data = []

    for month in sorted(monthly.keys()):
        total = monthly[month]['total']
        present = monthly[month]['present']
        percent = round((present / total) * 100, 2) if total else 0
        labels.append(month)
        data.append(percent)

    return labels, data



from collections import defaultdict


def get_continuous_absent_summary(attendance_qs, students_qs):
    """
    Calculates continuous absenteeism per class & section.

    Returns:
    {
      (class_name, section): {
          'gt2': int,
          'gt3': int,
          'gt4': int,
          'gt5': int
      }
    }
    """

    # Map attendance by student (latest first)
    attendance_map = defaultdict(list)
    for a in attendance_qs.order_by('-attendance_date'):
        attendance_map[a.Student_pen].append(a)

    summary = defaultdict(lambda: {
        'gt2': 0, 'gt3': 0, 'gt4': 0, 'gt5': 0
    })

    for s in students_qs:
        records = attendance_map.get(s.student_pen, [])
        continuous_absent = 0

        for r in records:
            if r.status != 'P':
                continuous_absent += 1
            else:
                break

        key = (s.student_class, s.section)

        if continuous_absent > 2:
            summary[key]['gt2'] += 1
        if continuous_absent > 3:
            summary[key]['gt3'] += 1
        if continuous_absent > 4:
            summary[key]['gt4'] += 1
        if continuous_absent > 5:
            summary[key]['gt5'] += 1

    return summary
