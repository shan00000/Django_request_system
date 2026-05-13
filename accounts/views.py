from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import UserProfile

# Create your views here.

def login_view(request):
    return render(request, "accounts/login.html")