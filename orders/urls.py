from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signUp", views.signUp, name="signUp"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("myOrders", views.myOrdersView, name="my_orders_view"),
    path("menu", views.menuView, name="menu"),
    path("order", views.orderView, name="order"),
    path("order/regularPizza", views.orderRegularPizzaView, name="order_regular_pizza"),
    path("order/pasta", views.orderPastaView, name="order_pasta"),
    path("order/checkout", views.checkoutView, name="checkout"),
    path("addCart", views.addCart, name="add_cart"),
    path("removeCart", views.removeCart, name="remove_cart"),
    path("checkoutCart", views.checkoutCart, name="checkout_cart"),
    path("adminOrder", views.adminOrderView, name="admin_order_view"),
    path("changeOrderStatus", views.changeOrderStatus, name="change_order_status"),
    path("orderDetails", views.orderDetails, name="order_details")
]