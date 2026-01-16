from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import UserCredential
from django.contrib.auth.decorators import login_required
from .models import Student

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserCredential
from .utils import (
    get_student_attendance_summary,
    get_longest_attendance_streak,
    get_student_marks_summary
)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user_record = UserCredential.objects.filter(
            username__iexact=username
        ).first()

        if not user_record:
            messages.error(request, 'User not found')
            return render(request, 'login_page.html')

        if password != user_record.password:
            messages.error(request, 'Invalid password')
            return render(request, 'login_page.html')

        user, _ = User.objects.get_or_create(username=user_record.username)
        login(request, user)

        # ✅ store role in session
        request.session['role'] = user_record.role

        return redirect('dashboard')

    return render(request, 'login_page.html')

def user_logout(request):

    logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('login')

@login_required
def dashboard(request):
    role = request.session.get('role', 'User')
    return render(request, 'dashboard.html', {'role': role})

# def dashboard(request):
#     return render(request, 'dashboard.html')

@login_required
def student_info(request):
    view_type = request.GET.get('view_type')
    context = {}

    if view_type == 'individual':
        student_id = request.GET.get('student_id')
        student_name = request.GET.get('student_name')

        if student_id or student_name:
            qs = Student.objects.all()

            if student_id:
                qs = qs.filter(student_pen=student_id)

            if student_name:
                qs = qs.filter(name__icontains=student_name)

            student = qs.first()

            if student:
                total_days, present_days, absent_days = get_student_attendance_summary(student.student_pen)
                longest_streak = get_longest_attendance_streak(student.student_pen)

                marks_summary, subject_marks = get_student_marks_summary(student.student_pen)

                context.update({
                    'show_dashboard': True,
                    'student': student,
                    'total_working_days': total_days,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'longest_streak': longest_streak,
                    'total_marks': marks_summary['total_marks'],
                    'marks_obtained': marks_summary['obtained_marks'],
                    'subject_marks': subject_marks,
                    'attendance_present': present_days,
                    'attendance_absent': absent_days
                })
            else:
                context['no_data'] = True

    return render(request, 'student_info.html', context)

@login_required
def fee_payment(request):
    return render(request, 'fee_payment.html')

@login_required
def update_student(request):
    return render(request, 'update_student.html')

@login_required
def data_analysis(request):
    return render(request, 'data_analysis.html')
