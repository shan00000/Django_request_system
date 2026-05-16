from django.urls import path
from .views import DashboardView, logout_view, RequestDetailView, NewRequestView


app_name = "requests"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("new/", NewRequestView.as_view(), name="new_request"),
    path("request/<int:pk>/", RequestDetailView.as_view(), name="request_detail"),
]