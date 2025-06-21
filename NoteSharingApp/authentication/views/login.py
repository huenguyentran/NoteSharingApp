from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from ..forms import LoginForm
from ..forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



class LoginView(View):
  def get(self, request):
    return redirect('auth_combined')

  def post(self, request):
    login_new_form = LoginForm()
    register_new_form = RegistrationForm()

    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        username = login_form.data.get('login_username')
        password = login_form.data.get('login_password')
        user = authenticate(request, username=username, password=password) 
        if user:
            login(self.request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        messages.error(request, "Vui lòng nhập đúng định dạng.")
        context = {
            'login_form': login_new_form, 
            'register_form': register_new_form 
        }
        return render(request, self.template_name, context)
