from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=65) 
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=65, widget=forms.PasswordInput)   
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

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise forms.ValidationError("New password and confirmation do not match.")
        
        return cleaned_data
