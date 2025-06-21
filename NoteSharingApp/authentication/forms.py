from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    login_username = forms.CharField(max_length=65)
    login_password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    res_username = forms.CharField(max_length=65) 
    res_password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    res_confirm_password = forms.CharField(max_length=65, widget=forms.PasswordInput)   

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Tên đăng nhập đã tồn tại.')
        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Mật khẩu xác nhận không khớp.")
        return cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(max_length=65, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        old_password = cleaned_data.get('old_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
   
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Mật khẩu cũ không đúng.")
        
        if new_password != confirm_new_password:
            raise forms.ValidationError("Mật khẩu mới và xác nhận mật khẩu không khớp.")
        
        return cleaned_data
    
class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }