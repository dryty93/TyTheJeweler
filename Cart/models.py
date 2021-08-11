import os
import sys
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from django_mysql.models import ListCharField
from django.db.models import CharField, Model
from djmoney.money import Money
from Products.models import Product
from django.utils.text import slugify
from django.dispatch import receiver
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.contrib.auth.models import User
sys.path.append(os.path.realpath('.'))
#from tythejeweler.Products.models import *
from django.db import models
from django.utils import timezone
# Create your models here.


class CartEntry (models.Model):

    product= models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#    selected = models.BooleanField(default=False)
    price = MoneyField( max_digits=14, decimal_places=2, default_currency='USD')
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    session = models.CharField(max_length=51, default="")
    date = models.DateTimeField(default=timezone.now)

   # selected = models.BooleanField(default=False, null=True)


    def __str__(self):
        return f'{self.product}'




class Cart(models.Model):

    order_items = models.ManyToManyField(CartEntry)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_data = models.JSONField(null=True)
    trans_id= models.IntegerField(default=0)
    total_cost = MoneyField( max_digits=14, decimal_places=2, default_currency='USD')





    def __str__(self):

        product_id = self.order_items.all().values("product_id")
        product = Product
        prod_list = []
        for products in product_id:
            prod_list.append(product.objects.filter(id=products['product_id']))


        return f'{self.user, prod_list}'

class Order(models.Model):
   # order_items = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    destination = models.TextField(default="")
    price = models.IntegerField(default=0)
    success= models.BooleanField(default=False)

    def __str__(self):

        return f'{self.created, self.user}'

"""
@receiver(sender= CartEntry,signal=post_save)
def addToCart(sender, instance, **kwargs):
    shopper = instance.user
    all_items = CartEntry.objects.filter(user=shopper)
    session  = all_items.values('session')
    total_query = all_items.values('price')

    total = 0


    for prices in total_query:
        total += prices['price']

    new_cart = Cart.objects.create(user=shopper, total_cost=total)
    new_cart.total_cost_currency= 'USD'


#    new_cart.order_items.set(all_items.values("product"))

    #print(new_cart.order_items)

                                        #     price=price_dec, user=request.user, session=session_id)


    post_save.disconnect(addToCart, sender=Cart)
   # instance.quantity -=1

 #   if  instance.quantity == 0:

    new_cart.save()

    post_save.connect(addToCart, sender=Cart)



"""
