from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User 
from ..forms import RegistrationForm, LoginForm



class CombinedAuthView(View):
    template_name = 'accounts/login_register.html'

    
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()

        register_form = RegistrationForm()
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, self.template_name, context)


