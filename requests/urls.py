from django.urls import path
from .views import DashboardView, RequestDetailView, NewRequestView, EditRequestView 
from .views import logout_view, renew_request_view


app_name = "requests"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("request/<int:pk>/renew/", renew_request_view, name="renew_request"),
    path("new/", NewRequestView.as_view(), name="new_request"),
    path("request/<int:pk>/", RequestDetailView.as_view(), name="request_detail"),
    path("request/<int:pk>/edit/", EditRequestView.as_view(), name="edit_request"),
]