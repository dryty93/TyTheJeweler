from django.contrib import admin
from .models import Product,Material,Category
# Register your models here.

admin.site.register(Product)
admin.site.register(Material)
admin.site.register(Category)