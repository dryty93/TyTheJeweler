from django import forms
from .models import Product
from Cart.models import CartEntry, Cart
from paypal.standard.forms import PayPalPaymentsForm



class CartAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(CartAddForm, self).__init__(*args, **kwargs)


    def save(self, *args, **kw):
        return self.instance

    class Meta:

        model = CartEntry

        fields = ['product', 'price']




