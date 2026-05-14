from django.urls import path
from .views import DashboardView, logout_view


app_name = "requests"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("logout/", logout_view, name="logout"),
]