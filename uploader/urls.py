#
#
# from django.urls import path
# from . import views
# from . import views
#
# urlpatterns = [
#     path('', views.user_login, name='login'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('student-info/', views.student_info, name='student_info'),
#     path('fee-payment/', views.fee_payment, name='fee_payment'),
#     path('update-student/', views.update_student, name='update_student'),
#     path('data-analysis/', views.data_analysis, name='data_analysis'),
#     path('dashboard/school/',views.school_dashboard,name='school_dashboard'),
#     path('dashboard/school/class/',views.class_drill_dashboard,name='class_drill_dashboard'),
#     path('dashboard/school/export/',views.export_school_dashboard_excel,name='export_school_dashboard_excel'),
#     path("staff/", views.staff_fee_dashboard, name="fee_dashboard"),
#     path("pay/<int:student_fee_id>/", views.pay_fee, name="pay_fee"),
#     path("receipt/<int:payment_id>/", views.fee_receipt, name="fee_receipt"),
#     path("reports/daily-collection/", views.daily_collection_report, name="daily_collection_report"),
#     path("fees/authority/", views.authority_fee_dashboard, name="authority_fee_dashboard"),
#     path("fees/authority/chart/", views.authority_fee_chart_data, name="authority_fee_chart"),
#     path("fees/authority/students/", views.authority_fee_students, name="authority_fee_students"),
#     path("fees/authority/export/", views.authority_fee_export_excel, name="authority_fee_export"),
#     path("fees/authority/student/<int:student_id>/", views.authority_student_profile, name="authority_student_profile"),
#
# ]

from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # AUTH
    # =========================
    path("", views.user_login, name="login"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # =========================
    # DASHBOARD (HOME)
    # =========================
    path("dashboard/", views.dashboard, name="dashboard"),

    # =========================
    # STUDENT INFO
    # =========================
    path("student-info/", views.student_info, name="student_info"),

    # =========================
    # SCHOOL ATTENDANCE DASHBOARD
    # =========================
    path("school-dashboard/", views.school_dashboard, name="school_dashboard"),
    path(
        "school-dashboard/export/",
        views.export_school_dashboard,
        name="export_school_dashboard"
    ),

    # =========================
    # STAFF FEE DASHBOARD
    # =========================
    path("fees/", views.fee_dashboard, name="fee_dashboard"),
    path("pay/<int:student_fee_id>/", views.pay_fee, name="pay_fee"),
    path(
        "fees/receipt/<int:payment_id>/",
        views.fee_receipt,
        name="fee_receipt"
    ),

    # =========================
    # DAILY COLLECTION REPORT
    # =========================
    path(
        "fees/daily-collection/",
        views.daily_collection_report,
        name="daily_collection_report"
    ),
    path(
        "management/fees/",
        views.management_fee_dashboard,
        name="management_fee_dashboard",
    ),
    path(
        "management/fees/student/<str:student_pen>/",
        views.management_student_fee_detail,
        name="management_student_fee_detail",
    ),

    # =========================
    # AUTHORITY FEE DASHBOARD
    # =========================
    path(
        "authority/",
        views.authority_fee_dashboard,
        name="authority_fee_dashboard"
    ),

    path(
        "authority/chart/",
        views.authority_fee_chart_data,
        name="authority_fee_chart_data"
    ),

    # =========================
    # CLASS DRILL DASHBOARD
    # =========================
    path(
        "authority/class-drill/",
        views.class_drill_dashboard,
        name="class_drill_dashboard"
    ),

path(
        "authority/regular-absent-drill/",
        views.regular_absent_drill,
        name="regular_absent_drill"
    ),


    # =========================
    # DRILL: CLASS → STUDENTS
    # =========================
    path(
        "authority/students/",
        views.authority_fee_students,
        name="authority_fee_students"
    ),

    # =========================
    # DRILL: STUDENT PROFILE
    # =========================
    path(
        "authority/student/<int:student_id>/",
        views.authority_student_profile,
        name="authority_student_profile"
    ),

    # =========================
    # AUTHORITY EXPORT
    # =========================
    path(
        "authority/export/",
        views.authority_export_excel,
        name="authority_export_excel"
    ),
    # =========================
    # ATTENDENCE UPDATE
    # =========================

    path("attendance/", views.mark_attendance, name="mark_attendance"),
    path(
        "attendance/export/",
        views.export_attendance_excel,
        name="export_attendance_excel"
    ),

## performamce dashbaord

    path(
        "dashboard/class-performance/",
        views.class_performance_dashboard,
        name="class_performance_dashboard"
    ),
    path(
        "dashboard/api/class-performance/",
        views.class_performance_api,
        name="class_performance_api"
    ),
    path(
        "dashboard/api/subject-performance/",
        views.subject_performance_api,
        name="subject_performance_api"
    ),
    path(
        "dashboard/export/class-performance/",
        views.export_class_performance_excel,
        name="export_class_performance_excel"
    ),
    path(
        "dashboard/api/student-wise-marks/",
        views.student_wise_marks_api,
        name="student_wise_marks_api"
    ),

]
