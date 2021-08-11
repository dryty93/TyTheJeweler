from django.contrib import admin
from .models import CartEntry, Cart, Order

admin.site.register(CartEntry)
admin.site.register(Order)
admin.site.register(Cart)
