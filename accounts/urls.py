from django.urls import path
from .views import LoginView, RegisterUser


app_name = "accounts"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
]