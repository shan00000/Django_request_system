from django.urls import path
from .views import DashboardView


app_name = "requests"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]