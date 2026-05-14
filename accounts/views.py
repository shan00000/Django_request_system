from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import time
# Create your views here.



class LoginView(generic.TemplateView):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, self.template_name, {"error_message": "Invalid username or password."})
        elif not user.userprofile.is_approved:
            return render(request, self.template_name, {"error_message": "Your account is awaiting admin approval. Please try again later."})
        elif user.userprofile.role == "cms_it":
            login(request, user)
            return redirect("admin:index")
        else:
            login(request, user)
            return HttpResponse("Login successful. You can now submit requests.")


        # if user is not None:
        #     login(request, user)
        #     return redirect("admin:index")
        # else:
        #     return render(request, self.template_name, {"error_message": "Invalid username or password."})

class RegisterUser(generic.TemplateView):
    template_name = "accounts/register.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        department = request.POST.get("department")

        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {"error_username": f"Username {username} already exists."})

        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error_email": f"Email {email} already exists."})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(
            user=user,
            department=department,
            role="academic",
            is_approved=False)
        
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        return render(request, self.template_name, {"submission_message": "Registration successful. Awaiting admin approval. Ones approved you can login."})
        
