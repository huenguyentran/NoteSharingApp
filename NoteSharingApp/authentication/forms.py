from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    login_username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={'placeholder': 'User name'}) # THÊM PLACEHOLDER
    )
    login_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) # THÊM PLACEHOLDER
    )

class RegistrationForm(forms.Form):
    res_username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={'placeholder': 'User name'}) # THÊM PLACEHOLDER
    )
    res_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}) # THÊM PLACEHOLDER
    )
    res_confirm_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}) # THÊM PLACEHOLDER
    )

    def clean_username(self):
        # LƯU Ý: Trường trong form là 'res_username', không phải 'username'
        username = self.cleaned_data.get('res_username') # ĐÃ SỬA TÊN TRƯỜNG TẠI ĐÂY
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Tên đăng nhập đã tồn tại.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        # LƯU Ý: Trường trong form là 'res_password' và 'res_confirm_password'
        password = cleaned_data.get("res_password") # ĐÃ SỬA TÊN TRƯỜNG TẠI ĐÂY
        confirm_password = cleaned_data.get("res_confirm_password") # ĐÃ SỬA TÊN TRƯỜNG TẠI ĐÂY

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('res_confirm_password', "Mật khẩu xác nhận không khớp.") # ĐÃ SỬA TÊN TRƯỜNG
        return cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu cũ'}) # THÊM PLACEHOLDER
    )
    new_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu mới'}) # THÊM PLACEHOLDER
    )
    confirm_new_password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'placeholder': 'Xác nhận mật khẩu mới'}) # THÊM PLACEHOLDER
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        # Dòng này bị lặp, chỉ cần một thôi
        # cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        old_password = cleaned_data.get('old_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if not self.user.check_password(old_password):
            self.add_error('old_password', "Mật khẩu cũ không đúng.") # Dùng add_error cho trường cụ thể
        
        if new_password and confirm_new_password: # Chỉ kiểm tra khi cả hai có giá trị
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', "Mật khẩu mới và xác nhận mật khẩu không khớp.")
        
        return cleaned_data
    
class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}), # THÊM PLACEHOLDER
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), # THÊM PLACEHOLDER
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}), # THÊM PLACEHOLDER
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}), # THÊM PLACEHOLDER
        }