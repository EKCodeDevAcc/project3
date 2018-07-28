from django.db import models
from django.conf import settings

# Create your models here.
class Menu(models.Model):
    menu_type = models.CharField(max_length = 64)
    menu_name = models.CharField(max_length = 64)
    menu_size = models.CharField(max_length = 64)
    menu_price = models.FloatField()

    def __str__(self):
        return f"{self.menu_type} {self.menu_name} {self.menu_size} {self.menu_price}"


class PizzaTopping(models.Model):
    pizza_topping_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.pizza_topping_name}"


class SubTopping(models.Model):
    sub_topping_name = models.CharField(max_length=64)
    sub_topping_price = models.FloatField()

    def __str__(self):
        return f"{self.sub_topping_name} {self.sub_topping_price}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    status = models.CharField(max_length = 64)
    order_price = models.FloatField()

    def __str__(self):
        return f"{self.user} {self.order_date} {self.status} {self.order_price}"


class Item(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_id")
    topping_pizza = models.ManyToManyField(PizzaTopping, blank=True, related_name="topping_pizza")
    topping_sub = models.ManyToManyField(SubTopping, blank=True, related_name="topping_sub")
    price_menu = models.FloatField()
    price_sub_topping = models.FloatField()

    def __str__(self):
        return f"{self.order_id} {self.menu_id} {self.topping_pizza} {self.topping_sub} {self.price_menu} {self.price_sub_topping}"