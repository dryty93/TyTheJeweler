


from django.urls import include, path
from . import views
from django.conf.urls import url

urlpatterns = [

    path('Cart/',views.cart, name='cart'),

    path('Cart/Checkout/', views.makeCart, name='makeCart'),
    path('Cart/process-payment/', views.process_payment, name='process_payment'),
    path('Cart/payment-done/', views.payment_done, name='payment_done'),
    path('Cart/payment-canceled/', views.payment_canceled, name='payment_canceled'),
    path('Cart/rem', views.rem,name='rem'),
    path('Cart/Order/', views.cart_to_order,name='cart_to_order'),


    # path('<int:aoi_id>/', views.one_aoi, name='one_aoi'),

    ]