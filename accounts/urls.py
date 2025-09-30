# accounts/urls.py
from django.urls import path

from .views.signin import Signin
from .views.signup import Signup
from .views.user import GetUser

app_name = "accounts"

urlpatterns = [
    path("signin", Signin.as_view(), name="signin"),
    path("signup", Signup.as_view(), name="signup"),
    path("user", GetUser.as_view(), name="user"),
]
