
from django.shortcuts import render
from .models import DataEntry

def upload_form(request):
    if request.method == "POST":
        DataEntry.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            amount=request.POST['amount']
        )
    return render(request, "form1.html")
