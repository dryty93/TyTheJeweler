from decimal import Decimal
from django.urls import reverse
from django.conf import settings

class CartLibrary():

    def paypal_connect(request,total,host,products):
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % Decimal(total).quantize(
                Decimal('.01')),
            'item_name': 'Cart {}'.format(products),
            'invoice': str(products),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'cancel_return': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        }
        return paypal_dict

