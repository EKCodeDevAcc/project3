from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signUp", views.signUp, name="signUp"),
    path("login", views.loginPost, name="login"),
    path("logout", views.logoutPost, name="logout")
]