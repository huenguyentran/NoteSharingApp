from .login import LoginView
from .registration import RegistrationView
#chuyen home sang core
from .home import HomeView
from .googleCallBack import GoogleCallbackView
from .googlLogin import GoogleLoginView
from .logout import LogoutView
from .account import AccountView
from .usernameValidation import UsernameValidationView
from .passwordValidation import PasswordValidationView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User 
from ..forms import RegistrationForm 
class CombinedAuthView(View):
    template_name = 'accounts/login_register.html'
    
    def get(self, request, *args, **kwargs):
        login_form = AuthenticationForm()

        register_form = RegistrationForm()
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = AuthenticationForm()

        register_form = RegistrationForm()

        if 'password2' in request.POST: 

            register_form = RegistrationForm(request.POST) 
            if register_form.is_valid():
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']

                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.')
                    context = {
                        'login_form': login_form, 
                        'register_form': register_form
                    }
                    return render(request, self.template_name, context)

                user = User.objects.create_user(username=username, password=password)

                user.backend = 'django.contrib.auth.backends.ModelBackend' 
                login(request, user)
                messages.success(request, f"Tài khoản {user.username} đã được tạo thành công!")
                return redirect('some_dashboard_url') 
            else:

                for field, errors in register_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

                context = {
                    'login_form': login_form, 
                    'register_form': register_form 
                }
                return render(request, self.template_name, context)
        else: 
        
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password) 
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Chào mừng trở lại, {username}!")
                    return redirect('some_dashboard_url')
                else:
                    messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
            else:
                messages.error(request, "Vui lòng nhập đúng định dạng.")
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, self.template_name, context)
