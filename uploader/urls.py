

from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student-info/', views.student_info, name='student_info'),
    path('fee-payment/', views.fee_payment, name='fee_payment'),
    path('update-student/', views.update_student, name='update_student'),
    path('data-analysis/', views.data_analysis, name='data_analysis'),
    path('dashboard/school/',views.school_dashboard,name='school_dashboard'),
    path('dashboard/school/class/',views.class_drill_dashboard,name='class_drill_dashboard'),
    path('dashboard/school/export/',views.export_school_dashboard_excel,name='export_school_dashboard_excel'),
    path("staff/", views.staff_fee_dashboard, name="fee_dashboard"),
    path("pay/<int:student_fee_id>/", views.pay_fee, name="pay_fee"),
    path("receipt/<int:payment_id>/", views.fee_receipt, name="fee_receipt"),
    path("reports/daily-collection/", views.daily_collection_report, name="daily_collection_report"),

]
#
# path('fees/', views.fee_dashboard, name='fee_dashboard'),
# path('fees/receipt/<int:fee_id>/', views.create_fee_receipt, name='create_fee_receipt'),

# from django.urls import path
# from .views import user_login, user_logout, dashboard
#
# urlpatterns = [
#     path('', user_login, name='login'),
#     path('login/', user_login, name='login'),
#     path('logout/', user_logout, name='logout'),
#     path('dashboard/', dashboard, name='dashboard'),
# ]
