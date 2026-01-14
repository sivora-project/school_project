from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import UserCredential

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserCredential

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user_record = UserCredential.objects.filter(
            username__iexact=username
        ).first()

        if not user_record:
            messages.error(request, 'User not found')
            return render(request, 'login.html')

        if password != user_record.password:
            messages.error(request, 'Invalid password')
            return render(request, 'login.html')

        user, _ = User.objects.get_or_create(username=user_record.username)
        login(request, user)

        # ✅ store role in session
        request.session['role'] = user_record.role

        return redirect('dashboard')

    return render(request, 'login_page.html')



def user_logout(request):
    logout(request)
    return redirect('login_page.html')


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    role = request.session.get('role', 'User')
    return render(request, 'dashboard.html', {'role': role})

# def dashboard(request):
#     return render(request, 'dashboard.html')

@login_required
def student_info(request):
    return render(request, 'student_info.html')

@login_required
def fee_payment(request):
    return render(request, 'fee_payment.html')

@login_required
def update_student(request):
    return render(request, 'update_student.html')

@login_required
def data_analysis(request):
    return render(request, 'data_analysis.html')
