from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Products.views import new_guest_user


guest = new_guest_user
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)
        self.fields['username'].initial = guest.username
                            
    
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email@email.com'}),
        }