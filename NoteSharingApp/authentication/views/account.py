from core.views.BaseView import BaseView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import View
from ..forms import AccountSettingsForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash

class AccountView(BaseView):
    template_name = 'accounts/account.html'

    def get(self, request):
        account_form = AccountSettingsForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
        password_form = ChangePasswordForm(user=request.user)
        return render(request, self.template_name, {
            'account_form': account_form,
            'password_form': password_form,
        })
    
    def post(self, request): 
        if 'update_account' in request.POST:
            return self.update_account(request)
        elif 'change_password' in request.POST:
            return self.change_password(request)
        return redirect('account_settings')
    
    def update_account(self, request):
        account_form = AccountSettingsForm(request.POST or None)
        password_form = ChangePasswordForm(user=request.user) # Initialize password form for display
        if account_form.is_valid():
            user = request.user
            user.email = account_form.cleaned_data.get('email')
            user.first_name = account_form.cleaned_data.get('first_name')
            user.last_name = account_form.cleaned_data.get('last_name')
            user.save()
            messages.success(request, "Account information has been updated.")
        else:
            messages.error(request, "Please enter complete information.")
        return render(request, self.template_name, {
            'account_form': account_form,
            'password_form': password_form,
        })
    
    def change_password(self, request):
        # Always re-initialize the account form to populate existing user data
        account_form = AccountSettingsForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
        password_form = ChangePasswordForm(user=request.user, data=request.POST or None)

        if password_form.is_valid():
            new_password = password_form.cleaned_data.get('new_password2') # Use new_password2 as per Django's ChangePasswordForm
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password has been changed successfully.")
            return redirect('account_settings')
        else:
            messages.error(request, "Incorrect information entered.")

        return render(request, self.template_name, {
            'account_form': account_form,
            'password_form': password_form,
        })