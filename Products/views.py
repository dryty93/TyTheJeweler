from django.shortcuts import HttpResponse, HttpResponseRedirect
from .models import Product,Category,Material
from django.template import loader
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from Cart.models import CartEntry
from .product_functions import Guest as g_u, getTotal


new_guest_user = g_u(False, 0, 0)

def make_guest(usr= new_guest_user):
    if new_guest_user:
        return usr
    else:

        print(usr)

name= make_guest(new_guest_user.username)

def index(request):

    template = loader.get_template("Products/index.html")
    if request.user.is_authenticated:
        user = request.user
        new_guest_user.visits += 1


    if not request.user.is_authenticated:

        new_guest_user.guest_flag = True

        user = new_guest_user

        if new_guest_user.visits <=1:

            new_guest_user.visits += 1
            guest = new_guest_user.create_guest_user(user= User)
            new_guest = User.objects.filter(username=user.username).values()
            print(user.username,new_guest_user.pk)

            new_guest_user.get_guest(new_guest_user)

        elif new_guest_user.visits >= 2:
            new_guest_user.guest_flag = False
            print(new_guest_user.username,'jh')
            count = 0
            entries = CartEntry.objects.filter(user=user.pk)

            total = getTotal(CartEntry.objects.filter(user=user.pk))

            for i in entries:
                count += 1
            context = {'name': user.username,'user': user.username, 'guest_flag': new_guest_user.guest_flag,
                       'entries': entries, 'total': total}
            print(user.username)
            return HttpResponse(template.render(context, request))
      #  entries = CartEntry.objects.filter(user=request.user)

        total = getTotal(CartEntry.objects.filter(user=user.pk))

        context = {'user': user, 'guest_flag': False,
                   'total': total, 'guest':new_guest_user}
        return HttpResponse(template.render(context, request))


    elif request.user.is_authenticated:
        entries = CartEntry.objects.filter(user=user)
        guest_flag=False
        print('found', user)

        count = 0
        entries = CartEntry.objects.filter(user=user.pk)
    
        total = getTotal(CartEntry.objects.filter(user=user.pk))
        
        for i in entries:
            count += 1
        context = {'user':user, 'guest_flag':new_guest_user.guest_flag,
                   'entries': entries, 'count': count, 'total':total}
        print(user.username)
        return HttpResponse(template.render(context, request))
    


class MaterialList(ListView):

    model= Material

class MaterialDetail(DetailView):
    model = Material


def product_page(request):
    template = loader.get_template("Products/products.html")
    products = Product.objects.all()
    header = request.headers
    user= request.user
    cookies= header['Cookie']
    if not user.is_authenticated:
        user = make_guest().pk

    categories = Category.objects.all()
    material = Material.objects.all()

    entries = CartEntry.objects.filter(user=user)

    total = getTotal(entries)

    context = { 'products':products, 'categories': categories, 'material':material, 'entries':entries, 'total':total}
    return HttpResponse(template.render(context, request))

def det_view( request, product_id):

    template = loader.get_template("Products/detailed_product_page.html")
    id= product_id
    product =Product.objects.get(id=id)
    product_name = product
    context = {'product':product, "product_name":product_name,  }


    return HttpResponse(template.render(context, request))

def category_page(request):
    template = loader.get_template("Products/categories.html")
    products = Product.objects.all()
    categories = Category.objects.all()
    material = Material.objects.all()
    context = {'products':products, 'categories': categories, 'material':material}
    return HttpResponse(template.render(context, request))

def det_cat_view(request, category_id):

    template = loader.get_template("Products/cat_view.html")
    id = category_id
    category = Category.objects.get(id=id)
    cat_name = category
    products = Product.objects.filter(category_id=id)
    print(products)

    context = {'products':products,'category': category, "cat_name": cat_name}

    return HttpResponse(template.render(context, request))
