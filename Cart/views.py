from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core import serializers
from .models import CartEntry, Cart, Order
from Products.models import Product
from Products.views import make_guest
from .forms import CartAddForm
from datetime import datetime
from paypal.standard.ipn.signals import valid_ipn_received
from django.template import loader
from django.shortcuts import redirect,get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from .cart_functions import CartLibrary
from Products.product_functions import Guest as p_f, getTotal
from random import  *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from djmoney.models.managers import understands_money

new_guest_user = make_guest()

print(new_guest_user)

@login_required(redirect_field_name='/login/')
def process_payment(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    entries = CartEntry.objects.filter(user=user)
    total = getTotal(entries)
    all_items = CartEntry.objects.filter(user= request.user).order_by('-date')
    order= cart
    host = request.get_host()
    cart_lib = CartLibrary()
    prod_list = []
    for items in entries:
        prod = Product.objects.get(id=items.product_id)
        prod_list.append(str(prod.name) + ' price ' + str(prod.price.amount))

    paypal_dict = cart_lib.paypal_connect(total,host,prod_list)
    paypal_dict['notify_url'] = 'http://127.0.0.1:8000/',

    valid = valid_ipn_received
    form = PayPalPaymentsForm(initial=paypal_dict)

    new_order = Order.objects.create(user=request.user,price=total, success=True)
    new_order.save()
    cart.delete()
    context = {'order':new_order, 'form':form,'paypal_dict':paypal_dict}

    return render(request, 'Cart/cart.html', {'all_items':all_items, 'order': cart,"total":total, 'form': form, 'paypal_dict':paypal_dict})

@csrf_exempt
def payment_done(request):
    return render(request, 'Cart/succes.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'Cart/cart.html')

@login_required(redirect_field_name='/login/')
def cart_to_order(request):

    current_cart = Cart.objects.latest('pk')
    cart_entries = CartEntry.objects.filter(cart = current_cart)
    current_cart.total = 0.00
    new_order = Order.objects.create(user=request.user)
    new_order.created = datetime.now()

    new_order.order_items = current_cart
    #new_order.set()
    new_order.save()
    current_cart.delete()
    #current_cart.save()
    total = 0

    return redirect("Cart/succes.html")
@login_required(redirect_field_name='/login/')
def rem(request):

    user = request.user
    if not user.is_authenticated:
        request.user= new_guest_user.pk
    all_items= CartEntry.objects.filter(user=request.user)
    count = 0
    select = []

    all_selected = {}
    if request.method == "POST":

        for items in request.POST.keys():
            if "csrf" not in items:
                if items not in select:
                    product = Product.objects.get(id=items)
                    del_entry=CartEntry.objects.get(product=items)
                    print(del_entry)
                #


                    CartEntry.objects.filter(product=product).delete()
                    product.amt_in_stock += 1
                    product.save()
                    del_entry.delete()


            select.append(items)



        #  if selected_items in i.product.name:

             #   CartEntry.objects.filter(pk=i.id).delete()

        return redirect("/Cart/")

@login_required(redirect_field_name='/login/')
def cart(request):


    all_items = CartEntry.objects.filter(user= request.user).order_by('-date')
    user=request.user
    total = 0.00
    for amt in all_items:
        print(amt.user)
        total += amt.price
    template = loader.get_template('Cart/cart.html')
    price_list = []

    if request.method == 'POST':
        print('wo')
        form = CartAddForm(request.POST)
        prod_name = request.POST["name"]
        price = request.POST["price"]
        price_dec = float(price[2:])
        id = request.POST['name']
        product = Product.objects.get(id=id)
        new_cart_item = CartEntry.objects.create(product=Product.objects.get(id=id),
                                                     price=price_dec, user=request.user)

        if product.amt_in_stock > 0:
            print(product.amt_in_stock)
            new_cart_item.save()
            product.amt_in_stock -= 1
            product.save()
            messages.add_message(request, messages.INFO,  'Added to Cart')
            print(messages.success(request, 'Added to Cart'))

            price_list.append(new_cart_item.price)

            for prices in price_list:
                total += new_cart_item.price
                print(price_list)

            if new_cart_item:
                return redirect('/Products')

            for prices in price_list:
                total += prices

        else:
            pass

        cart_lib = CartLibrary()
        host = request.get_host()
        prod_list = []
        entries = CartEntry.objects.filter(user=user)

        for items in entries:
                prod = Product.objects.get(id=items.product_id)
                prod_list.append(str(prod.name) + ' price ' + str(prod.price.amount))
        try:
            paypal_dict = cart_lib.paypal_connect(total.amount,host,prod_list)
            context={'all_items': all_items,'paypal_dict':paypal_dict, 'total': total, 'user':user, 'messages':messages}

        except:
            paypal_dict={}
    context={'all_items': all_items,'paypal_dict':"", 'total': total, 'user':user, 'messages':messages}



    return HttpResponse(template.render(context, request))
    context= {'all_items': all_items}

@login_required(redirect_field_name='/login/')
def makeCart(request):

    user = request.user

    if user.is_authenticated:
        shopper = user
        all_items = CartEntry.objects.filter(user=shopper)


    elif not user.is_authenticated:
        shopper = User.objects.get(username=User.objects.get(id=new_guest_user.pk))

        all_items = CartEntry.objects.filter(user=shopper)

    total_query = all_items.values('price')
    template =  loader.get_template("Cart/checkout.html")

    total = 0.00
    product_list = []

    for items in all_items:
        product_list.append(items)

    for prices in total_query:
        total += float(prices['price'])

    new_cart = Cart.objects.create(user=shopper, total_cost=total)

    new_cart.save()
    new_cart.order_items.set(all_items)
    paypal_form = PayPalPaymentsForm()
    context = {'paypal_form': paypal_form, 'all_items' : all_items, 'total_query': total_query, 'total': total,
               'new_cart': new_cart}

    return HttpResponse(template.render(context, request))
