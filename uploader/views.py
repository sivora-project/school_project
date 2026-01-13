from django.shortcuts import render
from .models import DataEntry

def upload_form(request):
    error = None

    if request.method == "POST":
        try:
            DataEntry.objects.create(
                name=request.POST.get('name', ''),
                email=request.POST.get('email', ''),
                amount=int(request.POST.get('amount', 0))
            )
        except Exception as e:
            error = str(e)

    return render(request, "form.html", {"error": error})