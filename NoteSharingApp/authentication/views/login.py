from ..forms import LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        
        if user:
          login(self.request, user)
          return super().form_valid(form)
        else:
          messages.error(self.request, 'Đăng nhập thất bại')
          return super().form_invalid(form)
