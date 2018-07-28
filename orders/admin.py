from django.contrib import admin

from .models import Menu, PizzaTopping, SubTopping, Order, Item

# Register your models here.
admin.site.register(Menu)
admin.site.register(PizzaTopping)
admin.site.register(SubTopping)
admin.site.register(Order)
admin.site.register(Item)