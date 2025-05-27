from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=65) 
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=65, widget=forms.PasswordInput)   
