from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
# Create your views here.


# @login_required
# def dashboard(request):
#     return HttpResponse("Welcome to the dashboard! This is where you can view and manage your requests.")

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "requests/dashboard.html"
