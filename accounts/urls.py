from django.urls import path
from .views import LoginView, register_user


app_name = "accounts"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", register_user, name="register"),
]