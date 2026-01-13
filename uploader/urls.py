
from django.urls import path
from .views import upload_form

urlpatterns = [
    path('', upload_form),
]
