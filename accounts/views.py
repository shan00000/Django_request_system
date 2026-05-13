from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout

# Create your views here.



class LoginView(generic.TemplateView):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("admin:index")
        else:
            return render(request, self.template_name, {"error": "Invalid username or password."})

def register_user(request):
    return HttpResponse("User registration page")