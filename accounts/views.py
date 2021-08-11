from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import backends
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth.views import auth_login
from django.template import loader
from .forms import SignUpForm

class SignUp(FormView):
    template_name = "Products/signup.html"
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self,form):
        print(form.cleaned_data)
        new_user= User.objects.create_user( form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
        print(new_user.username)
       # form.save()

        return super().form_valid(form)




class Login(LoginView):

    def get(self, request, *args, **kwargs):
        user = request.user
        auth_login(user=user)
        template_name =  "login.html"
        return user

class Logout(LogoutView):
     template_name ="Products/logout.html"
     def logout(self):
        self.get_next_page("Products/")
     



class PassChange(TemplateView):
    template_name = "/accounts/pass_change.html"

class PassChangeSuccess(TemplateView):
    template_name = "/accounts/pass_change_success.html"

class PassReset(TemplateView):
    template_name = "/accounts/pass_reset.html"

class PassResetDone(TemplateView):
    template_name = "/accounts/pass_reset_done.html"

class PassResetConfirm(TemplateView):
    template_name="/accounts/pass_reset_confirm"
# Create your views here.

