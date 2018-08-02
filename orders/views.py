from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers

import datetime

from .models import Menu, PizzaTopping, SubTopping, Order, Item

# Create your views here.
def index(request):
    # If user is not logged in, redirect him/her to login page.
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html')
    return render(request, 'orders/index.html')

# Sign Up Page.
def signUp(request):
    # If user is logged in, redirect him/her to main page with message.
    if request.user.is_authenticated:
        return render(request, 'orders/index.html', {'message': 'To sign up, you have to logout first.'})
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'orders/signUp.html', {'form': form})

# Login Page.
def loginView(request):
    if request.user.is_authenticated:
        return render(request, 'orders/index.html', {'message': 'You already logged in.'})
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'orders/login.html', {'message': 'Invalid credentials.'})

# Logout
def logoutView(request):
    logout(request)
    return render(request, 'orders/login.html', {'message': 'You are logged out successfully.'})

# Checkout Page
def myOrdersView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # A list of orders belong to the current user.
    my_order = Order.objects.filter(user=request.user)
    context = {
        'my_orders' : my_order
    }
    return render(request, 'orders/my_orders.html', context)


# Order Details URL
def orderDetails(request):
    # Get id of selected order and get a list of items where its order id matches.
    order_id = request.GET.get('orderid')
    order_item = Item.objects.filter(item_order_id=order_id)
    order_item_length = Item.objects.filter(item_order_id=order_id).count()
    order_item_response = serializers.serialize("json", order_item)
    return HttpResponse(order_item_response, content_type='application/json')


# Menu Page.
def menuView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # To distinguish items depends on their menu type and size, get multiple objects and passed.
    regular_pizza_menu = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_name')
    regular_pizza_small = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_price')
    regular_pizza_large = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Large').only('menu_price')
    sicilian_pizza_menu = Menu.objects.filter(menu_type='Sicilian Pizza', menu_size='Small').only('menu_name')
    sicilian_pizza_small = Menu.objects.filter(menu_type='Sicilian Pizza', menu_size='Small').only('menu_price')
    sicilian_pizza_large = Menu.objects.filter(menu_type='Sicilian Pizza', menu_size='Large').only('menu_price')
    subs_menu = Menu.objects.filter(menu_type='Subs', menu_size='Large').only('menu_name')
    subs_small = Menu.objects.filter(menu_type='Subs', menu_size='Small').only('menu_price')
    subs_large = Menu.objects.filter(menu_type='Subs', menu_size='Large').only('menu_price')
    pasta_menu = Menu.objects.filter(menu_type='Pasta').only('menu_name')
    pasta_price = Menu.objects.filter(menu_type='Pasta').only('menu_price')
    salads_menu = Menu.objects.filter(menu_type='Salads').only('menu_name')
    salads_price = Menu.objects.filter(menu_type='Salads').only('menu_price')
    dinner_platters_menu = Menu.objects.filter(menu_type='Dinner Platters', menu_size='Large').only('menu_name')
    dinner_platters_small = Menu.objects.filter(menu_type='Dinner Platters', menu_size='Small').only('menu_price')
    dinner_platters_large = Menu.objects.filter(menu_type='Dinner Platters', menu_size='Large').only('menu_price')
    context = {
        'regular_pizza_menus' : regular_pizza_menu,
        'regular_pizza_smalls' : regular_pizza_small,
        'regular_pizza_larges' : regular_pizza_large,
        'sicilian_pizza_menus' : sicilian_pizza_menu,
        'sicilian_pizza_smalls' : sicilian_pizza_small,
        'sicilian_pizza_larges' : sicilian_pizza_large,
        'subs_menus' : subs_menu,
        'subs_smalls' : subs_small,
        'subs_larges' : subs_large,
        'pasta_menus' : pasta_menu,
        'pasta_prices' : pasta_price,
        'salads_menus' : salads_menu,
        'salads_prices' : salads_price,
        'dinner_platters_menus' : dinner_platters_menu,
        'dinner_platters_smalls' : dinner_platters_small,
        'dinner_platters_larges' : dinner_platters_large
    }
    return render(request, 'orders/menu.html', context)


# Order Page.
def orderView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of items that user put in the cart, but not checkout yet.
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    context = {
        'my_orders' : my_order
    }
    return render(request, 'orders/order.html', context)


# Order Regular Pizza Page.
def orderRegularPizzaView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of regular pizza menus.
    regular_pizza_menu = Menu.objects.filter(menu_type='Regular Pizza')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    # Get a list of pizza toppings.
    pizza_topping = PizzaTopping.objects.all()
    pizza_topping_length = PizzaTopping.objects.all().count()
    context = {
        'regular_pizza_menus' : regular_pizza_menu,
        'pizza_toppings' : pizza_topping,
        'pizza_topping_length' : pizza_topping_length,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_regular_pizza.html', context)


# Order Sicilian Pizza Page.
def orderSicilianPizzaView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of sicilian pizza menus.
    sicilian_pizza_menu = Menu.objects.filter(menu_type='Sicilian Pizza')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    pizza_topping = PizzaTopping.objects.all()
    pizza_topping_length = PizzaTopping.objects.all().count()
    context = {
        'sicilian_pizza_menus' : sicilian_pizza_menu,
        'pizza_toppings' : pizza_topping,
        'pizza_topping_length' : pizza_topping_length,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_sicilian_pizza.html', context)


# Order Subs Page.
def orderSubsView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of subs menus.
    subs_menu = Menu.objects.filter(menu_type='Subs')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    # Get a list of subs toppoings.
    sub_topping = SubTopping.objects.all()
    sub_topping_length = SubTopping.objects.all().count()
    context = {
        'subs_menus' : subs_menu,
        'sub_toppings' : sub_topping,
        'sub_topping_length' : sub_topping_length,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_subs.html', context)


# Order Pasta Page.
def orderPastaView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of pasta menus.
    pasta_menu = Menu.objects.filter(menu_type='Pasta')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    context = {
        'pasta_menus' : pasta_menu,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_pasta.html', context)


# Order Salads Page.
def orderSaladsView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of salads menus.
    salads_menu = Menu.objects.filter(menu_type='Salads')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    context = {
        'salads_menus' : salads_menu,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_salads.html', context)


# Order Dinner Platters Page.
def orderDinnerPlattersView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Get a list of dinner platters menus.
    dinner_platters_menu = Menu.objects.filter(menu_type='Dinner Platters')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    context = {
        'dinner_platters_menus' : dinner_platters_menu,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_dinner_platters.html', context)


# Add Cart URL
def addCart(request):
    # When a user select an item to put it in his/her cart, get information of the menu and create it as an item.
    item_type = request.GET.get('itemtype')
    item_name = request.GET.get('itemname')
    item_topping_pizza = request.GET.get('itempizzatopping')
    item_topping_sub = request.GET.get('itemsubtopping')
    item_size = request.GET.get('itemsize')
    item_price = request.GET.get('itemprice')
    item = Item.objects.create(username=request.user, item_type=item_type, item_menu_name=item_name, topping_pizza=item_topping_pizza, topping_sub=item_topping_sub, item_size=item_size, item_price=item_price, item_status='In Cart')
    return JsonResponse({'item_name': item_name, 'topping_pizza': item_topping_pizza, 'topping_sub': item_topping_sub, 'item_size':item_size, 'item_price': item_price})


# Remove Cart URL
def removeCart(request):
    # Get id of selected item from the cart and delete it from db.
    item_id = request.GET.get('itemid')
    Item.objects.get(id=item_id).delete()
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    order_length = Item.objects.filter(username=request.user, item_status='In Cart').count()
    return JsonResponse({'deleted_item_id': item_id})


# Checkout Cart URL
def checkoutCart(request):
    # When a user checkouts, create new order object.
    order_price = request.GET.get('orderprice')
    now = datetime.datetime.now()
    order = Order.objects.create(user=request.user, order_date=now, order_status='Order Placed', order_price=order_price)
    # Get id of lastest order.
    lastest_order = Order.objects.latest('id')
    order_id = lastest_order.id
    # Update order id and status of items in current user's cart.
    item = Item.objects.filter(username=request.user, item_status='In Cart').update(item_order_id=order_id, item_status='Order Placed')
    return JsonResponse({'order_stats': 'Complete'})


# Checkout Page
def checkoutView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    order_length = Item.objects.filter(username=request.user, item_status='In Cart').count()
    # Get prices of all menus in the cart, and add all prices.
    total_price = 0
    for i in range(order_length):
            total_price += my_order[i].item_price
    round_price = round(total_price, 2)
    two_decimal = "{:.2f}".format(round_price)
    context = {
        'my_orders' : my_order,
        'total_price': two_decimal
    }
    return render(request, 'orders/checkout.html', context)


# Admin Order Placed Page
# Limited to superuser
@user_passes_test(lambda user: user.is_superuser)
def adminOrderView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Display all orders whose status are Order Placed.
    all_order = Order.objects.filter(order_status='Order Placed')
    order_length = Order.objects.filter(order_status='Order Placed').count()
    context = {
        'all_orders' : all_order,
        'order_length' : order_length
    }
    return render(request, 'orders/admin_order.html', context)


# Admin Order Delivered Page
@user_passes_test(lambda user: user.is_superuser)
def adminOrderDeliveredView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    # Display all orders whose status are Delivered.
    all_order = Order.objects.filter(order_status='Delivered')
    order_length = Order.objects.filter(order_status='Delivered').count()
    context = {
        'all_orders' : all_order,
        'order_length' : order_length
    }
    return render(request, 'orders/admin_order_done.html', context)


# Change Order Status URL
def changeOrderStatus(request):
    order_status = request.GET.get('orderstatus')
    final_orders = request.GET.get('finalorders')
    # Get a list of choosen ids.
    id_list = [id.strip() for id in final_orders.split(',')]
    # Change status of order and its items depends what admin requested.
    for i in range(len(id_list)):
        Order.objects.filter(id=id_list[i]).update(order_status=order_status)
        Item.objects.filter(item_order_id=id_list[i]).update(item_status=order_status)
    return JsonResponse({'order_stats': 'Complete'})