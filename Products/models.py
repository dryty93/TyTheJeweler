from datetime import datetime

from djmoney.models.fields import MoneyField

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Material(models.Model ):
    name = models.CharField(max_length=300, null=False)
    summary = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='material_pics/')

    def __str__(self):
        return f'{self.name}'


class Category(models.Model ):
    name = models.CharField(max_length=300, null=False)
    summary = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='category_pics/')

    def __str__(self):
        return f'{self.name}'




class Product(models.Model ):
    name = models.CharField(max_length=300, null=False)
    summary = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='product_img/')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', name='price')
    material = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    amt_in_stock= models.IntegerField(default=1)
    slug = models.SlugField(null=True, default=name)

    def __str__(self):
        return f'{self.name}'

