from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserCredential
from .utils import (
    get_student_attendance_summary,
    get_longest_attendance_streak,
    get_student_marks_summary
)
from datetime import date, datetime
from django.shortcuts import render
from django.db.models import Count, Q

from .models import Student, Attendance, Classes
from .utils import get_continuous_absent_summary

from .models import Student, Attendance, AcademicCalendar
from .utils import (
    get_regular_absent_students,
    get_monthly_attendance_trend
)

from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
import openpyxl
from django.http import HttpResponse

from .models import Student, Attendance, AcademicCalendar, Classes
from .utils import update_fee_status
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.db import transaction
from datetime import date
import time

from .models import Student, StudentFee, FeePayment


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

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Student
from .utils import (
    get_student_attendance_summary,
    get_longest_attendance_streak,
    get_student_marks_summary
)


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Student
from .utils import (
    get_student_attendance_summary,
    get_longest_attendance_streak,
    get_student_marks_summary
)


@login_required
def student_info(request):
    view_type = request.GET.get('view_type')
    context = {}

    if view_type == 'individual':
        student_pen_input = request.GET.get('student_id')
        student_name = request.GET.get('student_name')
        month = request.GET.get('month')

        # ✅ NEW: exam filter (default FA1)
        exam_code = request.GET.get('exam_code', 'FA1')

        if student_pen_input or student_name:
            qs = Student.objects.all()

            if student_pen_input:
                qs = qs.filter(student_pen__iexact=student_pen_input)

            if student_name:
                qs = qs.filter(name__icontains=student_name)

            student = qs.first()

            if student:
                # ---------- ATTENDANCE ----------
                total_days, present_days, absent_days = get_student_attendance_summary(
                    student.student_pen, month
                )
                longest_streak = get_longest_attendance_streak(student.student_pen)

                # ---------- MARKS (FILTERED BY EXAM) ----------
                marks_summary, subject_marks = get_student_marks_summary(
                    student.student_id,
                    exam_code=exam_code
                )

                context.update({
                    'show_dashboard': True,
                    'student': student,

                    # attendance
                    'total_working_days': total_days,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'longest_streak': longest_streak,
                    'selected_month': month,

                    # marks
                    'total_marks': marks_summary['total_marks'],
                    'marks_obtained': marks_summary['obtained_marks'],
                    'subject_marks': subject_marks,
                    'selected_exam': exam_code,   # ✅ pass to UI
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




# =====================================================
# EXPORT TO EXCEL
# =====================================================
@login_required
def export_school_dashboard_excel(request):
    role = request.session.get('role')
    if role not in ['Admin', 'Principal', 'CEO']:
        return redirect('dashboard')

    selected_month = request.GET.get('month')
    today = date.today()
    month = int(selected_month) if selected_month else today.month

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Class Attendance"

    ws.append([
        "Class", "Section",
        "Total Students", "Present", "Absent", "Attendance %"
    ])

    classes = Classes.objects.filter(is_active=True)

    for cls in classes:
        students = Student.objects.filter(
            student_class__iexact=cls.class_name.strip(),
            section__iexact=cls.section.strip()
        )

        total = students.count()

        attendance = Attendance.objects.filter(
            Student_pen__in=students.values_list('student_pen', flat=True),
            attendance_date__month=month
        )

        present = attendance.filter(status='P').count()
        absent = total - present
        percent = round((present / total) * 100, 2) if total else 0

        ws.append([
            cls.class_name, cls.section,
            total, present, absent, percent
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=school_dashboard.xlsx'
    wb.save(response)
    return response


# =====================================================
# CLASS DRILL-THROUGH VIEW
# =====================================================
@login_required
def class_drill_dashboard(request):
    class_name = request.GET.get('class')
    section = request.GET.get('section')
    selected_month = request.GET.get('month')

    if not class_name or not section:
        messages.error(request, "Invalid class selection")
        return redirect('school_dashboard')

    today = date.today()
    month = int(selected_month) if selected_month else today.month

    students = Student.objects.filter(
        student_class__iexact=class_name,
        section__iexact=section
    )

    attendance = Attendance.objects.filter(
        Student_pen__in=students.values_list('student_pen', flat=True),
        attendance_date__month=month
    )

    present_ids = set(
        attendance.filter(status='P')
        .values_list('Student_pen', flat=True)
    )

    rows = []
    for s in students:
        rows.append({
            'student_pen': s.student_pen,
            'name': s.name,
            'status': 'Present' if s.student_pen in present_ids else 'Absent'
        })

    return render(request, 'class_drill_dashboard.html', {
        'class_name': class_name,
        'section': section,
        'student_rows': rows,
        'month': month
    })






MONTHS = [
    (1, "Jan"), (2, "Feb"), (3, "Mar"), (4, "Apr"),
    (5, "May"), (6, "Jun"), (7, "Jul"), (8, "Aug"),
    (9, "Sep"), (10, "Oct"), (11, "Nov"), (12, "Dec")
]

@login_required

def school_dashboard(request):
    today = date.today()

    # ---------------- SNAPSHOT FILTERS (TOP) ----------------
    snapshot_mode = request.GET.get('snapshot_mode', 'month')  # month / day
    snapshot_month = request.GET.get('snapshot_month')
    snapshot_date = request.GET.get('snapshot_date')

    if snapshot_mode == 'day' and snapshot_date:
        selected_date = datetime.strptime(snapshot_date, "%Y-%m-%d").date()
        snapshot_qs = Attendance.objects.filter(attendance_date=selected_date)
        snapshot_label = f"Date: {selected_date.strftime('%d %b %Y')}"
    else:
        snapshot_month = int(snapshot_month) if snapshot_month else today.month
        snapshot_qs = Attendance.objects.filter(
            attendance_date__month=snapshot_month
        )
        snapshot_label = f"Month: {dict(MONTHS)[snapshot_month]}"

    # ---------------- KPIs (SNAPSHOT) ----------------
    total_students = Student.objects.count()
    total_present = snapshot_qs.filter(status='P').count()
    total_absent = total_students - total_present
    attendance_percentage = round(
        (total_present / total_students) * 100, 2
    ) if total_students else 0

    # ---------------- CLASS TOTALS (MERGED A+B) ----------------
    class_totals = {}
    for cls in Classes.objects.filter(is_active=True):
        students = Student.objects.filter(
            student_class__iexact=cls.class_name.strip()
        )

        total_cls = students.count()
        class_att = snapshot_qs.filter(
            Student_pen__in=students.values_list('student_pen', flat=True)
        )

        present = class_att.filter(status='P').count()
        absent = total_cls - present
        percent = round((present / total_cls) * 100, 2) if total_cls else 0

        class_totals[cls.class_name] = {
            'total': total_cls,
            'present': present,
            'absent': absent,
            'percent': percent
        }

    # ---------------- CONTINUOUS ABSENTEES ----------------
    continuous_absent_map = get_continuous_absent_summary(
        snapshot_qs, Student.objects.all()
    )

    continuous_absent_rows = []
    for cls in Classes.objects.filter(is_active=True):
        for sec in ['A', 'B']:
            data = continuous_absent_map.get((cls.class_name, sec), {
                'gt2': 0, 'gt3': 0, 'gt4': 0, 'gt5': 0
            })
            continuous_absent_rows.append({
                'class_name': cls.class_name,
                'section': sec,
                **data
            })

    # ---------------- BAR CHART DATA (ABSENTEES) ----------------
    absent_bar_labels = [">2 Days", ">3 Days", ">4 Days", ">5 Days"]
    absent_bar_values = [
        sum(r['gt2'] for r in continuous_absent_rows),
        sum(r['gt3'] for r in continuous_absent_rows),
        sum(r['gt4'] for r in continuous_absent_rows),
        sum(r['gt5'] for r in continuous_absent_rows),
    ]

    # ---------------- TREND FILTERS (SEPARATE SECTION) ----------------
    trend_mode = request.GET.get('trend_mode', 'month')  # month / day
    trend_month = int(request.GET.get('trend_month', today.month))

    trend_labels, trend_data = [], []

    if trend_mode == 'day':
        daily = (
            Attendance.objects
            .filter(attendance_date__month=trend_month)
            .values('attendance_date')
            .annotate(
                total=Count('Student_pen'),
                present=Count('Student_pen', filter=Q(status='P'))
            )
            .order_by('attendance_date')
        )
        for d in daily:
            trend_labels.append(d['attendance_date'].strftime('%d %b'))
            trend_data.append(round((d['present'] / d['total']) * 100, 2))
    else:
        monthly = (
            Attendance.objects
            .values('attendance_date__month')
            .annotate(
                total=Count('Student_pen'),
                present=Count('Student_pen', filter=Q(status='P'))
            )
            .order_by('attendance_date__month')
        )
        for m in monthly:
            trend_labels.append(dict(MONTHS)[m['attendance_date__month']])
            trend_data.append(round((m['present'] / m['total']) * 100, 2))

    return render(request, "school_dashboard.html", {
        # Snapshot
        'months': MONTHS,
        'snapshot_mode': snapshot_mode,
        'snapshot_month': snapshot_month,
        'snapshot_date': snapshot_date,
        'snapshot_label': snapshot_label,

        'total_students': total_students,
        'total_present': total_present,
        'total_absent': total_absent,
        'attendance_percentage': attendance_percentage,

        'class_totals': class_totals,
        'continuous_absent_rows': continuous_absent_rows,

        # Charts
        'absent_bar_labels': absent_bar_labels,
        'absent_bar_values': absent_bar_values,

        # Trend
        'trend_mode': trend_mode,
        'trend_month': trend_month,
        'trend_labels': trend_labels,
        'trend_data': trend_data,
    })
# =====================================================
# FEE DASHBOARD
# =====================================================
@login_required
def fee_dashboard(request):

    academic_year = request.GET.get('academic_year')
    status = request.GET.get('status')

    fees = StudentFee.objects.select_related('fee_head')

    if academic_year:
        fees = fees.filter(academic_year=academic_year)

    if status:
        if status == 'DUE':
            fees = fees.filter(due_amount__gt=0)
        elif status == 'PAID':
            fees = fees.filter(due_amount=0)

    summary = fees.aggregate(
        total_fee=Sum('total_amount'),
        total_paid=Sum('paid_amount'),
        total_due=Sum('due_amount')
    )

    return render(request, 'fee_dashboard.html', {
        'fees': fees,
        'summary': summary
    })

# =====================================================
# CREATE FEE RECEIPT
# =====================================================
@login_required
def create_fee_receipt(request, fee_id):

    fee = StudentFee.objects.get(id=fee_id)

    if request.method == 'POST':
        amount = float(request.POST.get('amount'))

        FeePayment.objects.create(
            student_fee=fee,
            payment_date=date.today(),
            amount=amount,
            payment_mode=request.POST.get('payment_mode'),
            receipt_no=request.POST.get('receipt_no')
        )

        fee.paid_amount += amount
        update_fee_status(fee)

        messages.success(request, "Fee payment recorded successfully")
        return redirect('fee_dashboard')

    return render(request, 'fees/create_receipt.html', {
        'fee': fee
    })
def generate_receipt_no():
    """
    Format: RCPT-2025-000001
    """
    year = date.today().year

    last_payment = FeePayment.objects.order_by("-id").first()
    next_no = (last_payment.id + 1) if last_payment else 1

    return f"RCPT-{year}-{str(next_no).zfill(6)}"



def staff_fee_dashboard(request):
    student = None
    fee_rows = []

    if request.method == "POST":
        pen = request.POST.get("student_pen")

        student = Student.objects.filter(
            student_pen=pen
        ).first()

        if not student:
            return render(request, "fees/staff_fee_dashboard.html", {
                "error": "Invalid Student PEN"
            })

        fee_rows = (
            StudentFee.objects
            .filter(student_id=student.student_id)
            .select_related("fee_head")
            .order_by("term_no")
        )

    return render(request, "staff_fee_dashboard.html", {
        "student": student,
        "fee_rows": fee_rows
    })


def pay_fee(request, student_fee_id):
    student_fee = StudentFee.objects.filter(id=student_fee_id).first()
    if not student_fee:
        return HttpResponse("Fee record not found", status=404)

    student = Student.objects.filter(
        student_id=student_fee.student_id
    ).first()

    if not student:
        return HttpResponse("Student not found", status=404)

    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        mode = request.POST.get("payment_mode")
        utr = request.POST.get("utr")

        if amount > student_fee.due_amount:
            return render(request, "pay_fee.html", {
                "error": "Amount exceeds balance",
                "student_fee": student_fee,
                "student": student
            })

        with transaction.atomic():
            payment = FeePayment.objects.create(
                student_fee=student_fee,
                payment_date=date.today(),
                amount=amount,
                payment_mode=mode,
                receipt_no=f"RCPT-{date.today().year}-{student_fee_id}"
            )

            student_fee.paid_amount += amount
            student_fee.save()

        return redirect("fee_receipt", payment.id)

    return render(request, "pay_fee.html", {
        "student_fee": student_fee,
        "student": student
    })


def fee_receipt(request, payment_id):
    payment = FeePayment.objects.filter(id=payment_id).first()
    if not payment:
        return HttpResponse("Payment not found", status=404)

    student_fee = payment.student_fee
    student = Student.objects.filter(student_id=student_fee.student_id).first()

    return render(request, "fees/receipt.html", {
        "payment": payment,
        "student": student,
        "student_fee": student_fee
    })




def staff_fee_dashboard(request):
    student = None
    fee_rows = []
    selected_fee = None
    error = None

    # --------------------
    # SEARCH BY PEN
    # --------------------
    if request.method == "POST" and "student_pen" in request.POST:
        pen = request.POST.get("student_pen")

        student = Student.objects.filter(student_pen=pen).first()
        if not student:
            return render(request, "staff_fee_dashboard.html", {
                "error": "Invalid Student PEN"
            })

        fee_rows = StudentFee.objects.filter(
            student_id=student.student_id
        ).select_related("fee_head")

    # --------------------
    # PAY NOW CLICK
    # --------------------
    if request.method == "GET" and request.GET.get("pay"):
        fee_id = request.GET.get("pay")

        selected_fee = StudentFee.objects.filter(id=fee_id).first()
        if selected_fee:
            student = Student.objects.filter(
                student_id=selected_fee.student_id
            ).first()

            fee_rows = StudentFee.objects.filter(
                student_id=student.student_id
            ).select_related("fee_head")

    # --------------------
    # PAYMENT SUBMIT
    # --------------------


    # --------------------
    # PAYMENT SUBMIT
    # --------------------
    if request.method == "POST" and "amount" in request.POST:
        fee_id = request.POST.get("student_fee_id")
        amount = Decimal(request.POST.get("amount"))
        mode = request.POST.get("payment_mode")
        utr = request.POST.get("utr_number")

        selected_fee = StudentFee.objects.filter(id=fee_id).first()
        student = Student.objects.filter(
            student_id=selected_fee.student_id
        ).first()

        if amount > selected_fee.due_amount:
            error = "Amount exceeds balance"

        else:
            with transaction.atomic():
                receipt_no = generate_receipt_no()

                payment = FeePayment.objects.create(
                    student_fee=selected_fee,
                    payment_date=date.today(),
                    amount=amount,
                    payment_mode=mode,
                    receipt_no=receipt_no,
                    utr_number=utr if mode == "Non-Cash" else None
                )

                from django.db.models import F

                StudentFee.objects.filter(
                    id=selected_fee.id
                ).update(
                    paid_amount=F("paid_amount") + amount
                )

                # selected_fee.paid_amount += amount
                # selected_fee.save()


            return redirect("fee_receipt", payment_id=payment.id)

    return render(request, "staff_fee_dashboard.html", {
        "student": student,
        "fee_rows": fee_rows,
        "selected_fee": selected_fee,
        "error": error
    })


# --------------------
# RECEIPT PREVIEW
# --------------------
def fee_receipt(request, payment_id):
    payment = FeePayment.objects.filter(id=payment_id).first()
    student_fee = payment.student_fee
    student = Student.objects.filter(
        student_id=student_fee.student_id
    ).first()

    return render(request, "fee_receipt.html", {
        "payment": payment,
        "student": student,
        "student_fee": student_fee
    })
