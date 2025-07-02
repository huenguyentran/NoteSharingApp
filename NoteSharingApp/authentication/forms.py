from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    login_username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={'placeholder': 'User name'}) # ADD PLACEHOLDER
    )
    login_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) # ADD PLACEHOLDER
    )

class RegistrationForm(forms.Form):
    res_username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={'placeholder': 'User name'}) # ADD PLACEHOLDER
    )
    res_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) # ADD PLACEHOLDER
    )
    res_confirm_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}) # ADD PLACEHOLDER
    )

    def clean_username(self):
        # NOTE: The field in the form is 'res_username', not 'username'
        username = self.cleaned_data.get('res_username') # FIELD NAME CORRECTED HERE
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        # NOTE: The fields in the form are 'res_password' and 'res_confirm_password'
        password = cleaned_data.get("res_password") # FIELD NAME CORRECTED HERE
        confirm_password = cleaned_data.get("res_confirm_password") # FIELD NAME CORRECTED HERE

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('res_confirm_password', "Confirmation password does not match.") # FIELD NAME CORRECTED
        return cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Old password'}) # ADD PLACEHOLDER
    )
    new_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}) # ADD PLACEHOLDER
    )
    confirm_new_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}) # ADD PLACEHOLDER
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        # This line was duplicated, only one is needed
        # cleaned_data = super().clean() 
        new_password = cleaned_data.get('new_password')
        old_password = cleaned_data.get('old_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if not self.user.check_password(old_password):
            self.add_error('old_password', "Old password is incorrect.") # Use add_error for specific field
        
        if new_password and confirm_new_password: # Only check when both have values
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', "New password and confirmation do not match.")
        
        return cleaned_data
    
class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), # ADD PLACEHOLDER
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), # ADD PLACEHOLDER
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), # ADD PLACEHOLDER
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), # ADD PLACEHOLDER
        }