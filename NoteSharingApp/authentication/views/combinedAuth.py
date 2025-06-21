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

    def post(self, request, *args, **kwargs):
        login_form = LoginForm()

        register_form = RegistrationForm()

        if 'registration' in request.POST: 

            register_form = RegistrationForm(request.POST) 
            if register_form.is_valid():
                username = register_form.cleaned_data['res_username']
                password = register_form.cleaned_data['res_password']

                user = User.objects.create_user(username=username, password=password)

                user.backend = 'django.contrib.auth.backends.ModelBackend' 
                login(request, user)
                messages.success(request, f"Tài khoản {user.username} đã được tạo thành công!")
                return redirect('dashboard') 
            else:

                for field, errors in register_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

                context = {
                    'login_form': login_form, 
                    'register_form': register_form 
                }
                return render(request, self.template_name, context)
        elif 'login' in request.POST: 
        
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password) 
                if user:
                    login(self.request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
            else:
                messages.error(request, "Vui lòng nhập đúng định dạng.")
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, self.template_name, context)
