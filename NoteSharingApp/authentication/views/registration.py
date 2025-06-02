from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import login
from ..forms import RegistrationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm
    success_url = '/'
    def form_valid(self, form):
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      if User.objects.filter(username=username).exists():
        messages.error(self.request, 'Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.')
        return super().form_invalid(form)
      

      user = User.objects.create_user(username=username, password=password)
      user.backend = 'django.contrib.auth.backends.ModelBackend'
      login(self.request, user)
      return super().form_valid(form)

    def form_invalid(self, form):
      for field, errors in form.errors.items():
          for error in errors:
              messages.error(self.request, f"{field}: {error}")

      return super().form_invalid(form)