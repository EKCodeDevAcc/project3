from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
import datetime

from .models import Menu, PizzaTopping, SubTopping, Order, Item

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html')
    return render(request, 'orders/index.html')

# Sign Up Page.
def signUp(request):
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
        return render(request, 'orders/index.html', {'message': 'You already login.'})
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


# Menu Page.
def menuView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    regular_pizza_menu = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_name')
    regular_pizza_small = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_price')
    regular_pizza_large = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Large').only('menu_price')
    context = {
        'regular_pizza_menus' : regular_pizza_menu,
        'regular_pizza_smalls': regular_pizza_small,
        'regular_pizza_larges': regular_pizza_large
    }
    return render(request, 'orders/menu.html', context)


# Order Page.
def orderView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    regular_pizza_menu = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_name')
    regular_pizza_small = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_price')
    regular_pizza_large = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Large').only('menu_price')
    context = {
        'regular_pizza_menus' : regular_pizza_menu,
        'regular_pizza_smalls': regular_pizza_small,
        'regular_pizza_larges': regular_pizza_large
    }
    return render(request, 'orders/order.html', context)


# Order Regular Pizza Page.
def orderRegularPizzaView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    regular_pizza_menu = Menu.objects.filter(menu_type='Regular Pizza')
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    pizza_topping = PizzaTopping.objects.all()
    pizza_topping_length = PizzaTopping.objects.all().count()
    context = {
        'regular_pizza_menus' : regular_pizza_menu,
        'pizza_toppings' : pizza_topping,
        'pizza_topping_length' : pizza_topping_length,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_regular_pizza.html', context)


# Order Pasta Page.
def orderPastaView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    pasta_menu = Menu.objects.filter(menu_type='Pasta')
    my_order = Item.objects.filter(username=request.user)
    context = {
        'pasta_menus' : pasta_menu,
        'my_orders' : my_order
    }
    return render(request, 'orders/order_pasta.html', context)


# Add Cart URL
def addCart(request):
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
    item_id = request.GET.get('itemid')
    Item.objects.get(id=item_id).delete()
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    order_length = Item.objects.filter(username=request.user, item_status='In Cart').count()

    total_price = 0
    for i in range(order_length):
            total_price += my_order[i].item_price

    round_price = round(total_price, 2)
    two_decimal = "{:.2f}".format(round_price)

    return JsonResponse({'deleted_item_id': item_id, 'total_price': two_decimal})


# Checkout Cart URL
def checkoutCart(request):
    order_price = request.GET.get('orderprice')
    # now = datetime.datetime.now().strftime('%H:%M:%S')
    now = datetime.datetime.now()
    print('Now: ')
    print(now)
    order = Order.objects.create(user=request.user, order_date=now, order_status='Order Placed', order_price=order_price)
    lastest_order = Order.objects.latest('id')
    order_id = lastest_order.id
    print(order_id)
    item = Item.objects.filter(username=request.user, item_status='In Cart').update(item_order_id=order_id, item_status='Complete')

    return JsonResponse({'order_stats': 'Complete'})


# Checkout Page
def checkoutView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    my_order = Item.objects.filter(username=request.user, item_status='In Cart')
    order_length = Item.objects.filter(username=request.user, item_status='In Cart').count()

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


# Admin Order Page
# Limited to superuser
@user_passes_test(lambda user: user.is_superuser)
def adminOrderView(request):
    if not request.user.is_authenticated:
        return render(request, 'orders/login.html', {'message': 'Please login first.'})
    all_order = Order.objects.filter(order_status='Order Placed')

    context = {
        'all_orders' : all_order
    }
    return render(request, 'orders/admin_order.html', context)