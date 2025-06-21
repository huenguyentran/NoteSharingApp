from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class BaseView(LoginRequiredMixin, View):
    login_url = 'auth_combined'  
    redirect_field_name = 'next'  


    def get_context_data(self, **kwargs):
        context = kwargs
        context['user'] = self.request.user
        return context
