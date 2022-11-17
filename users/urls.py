from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("signup/", views.signup, name="signup"),
    path("", include("store.urls")),
]
