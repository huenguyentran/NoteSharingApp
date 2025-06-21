from django.contrib.auth import login
from django.contrib import messages 
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from ..forms import LoginForm
from ..forms import RegistrationForm


class RegisterView(View):
  template_name = 'accounts/login_register.html'

  def get(self, request):
    return redirect('auth_combined')

  def post(self, request):
    login_new_form = LoginForm()
    register_new_form = RegistrationForm()
        
    register_form = RegistrationForm(request.POST) 
    if register_form.is_valid():
        username = register_form.cleaned_data['res_username']
        password = register_form.cleaned_data['res_password']

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, f"Tài khoản {user.username} đã được tạo thành công!")
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('dashboard')
    else:

        for field, errors in register_form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")

        context = {
            'login_form': login_new_form, 
            'register_form': register_new_form 
        }
        return render(request, self.template_name, context)
    