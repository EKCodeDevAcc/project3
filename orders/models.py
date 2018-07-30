from django.db import models
from django.conf import settings

# Create your models here.
class Menu(models.Model):
    menu_type = models.CharField(max_length=64)
    menu_name = models.CharField(max_length=64)
    menu_size = models.CharField(blank=True, max_length=64)
    menu_price = models.FloatField()

    def __str__(self):
        return f"{self.menu_type} {self.menu_name} {self.menu_size} {self.menu_price}"


class PizzaTopping(models.Model):
    pizza_topping_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.pizza_topping_name}"


class SubTopping(models.Model):
    sub_topping_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sub_topping_name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=64)
    order_price = models.FloatField()

    def __str__(self):
        return f"{self.user} {self.order_date} {self.status} {self.order_price}"


class Item(models.Model):
    #item_order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name="item_order_id")
    item_order_id = models.PositiveIntegerField(blank=True, null=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #item_menu_name = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="item_menu_name")
    item_menu_name = models.CharField(max_length=64)
    topping_pizza = models.ManyToManyField(PizzaTopping, blank=True, related_name="topping_pizza")
    topping_sub = models.ManyToManyField(SubTopping, blank=True, related_name="topping_sub")
    quantity = models.IntegerField()
    item_price = models.FloatField()
    status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.item_order_id} {self.item_menu_name} {self.topping_pizza} {self.topping_sub} {self.item_price} {self.status}"