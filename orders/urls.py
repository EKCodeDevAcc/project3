from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signUp", views.signUp, name="signUp"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("menu", views.menuView, name="menu"),
    path("order", views.orderView, name="order"),
    path("order/pasta", views.orderPastaView, name="order_pasta"),
]