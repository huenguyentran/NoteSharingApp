# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\forms.py

from django import forms
from django.forms import ModelForm # Import ModelForm rõ ràng
from .models import Workspace, WorkspaceMember # Import tất cả các model cần thiết
from django.contrib.auth import get_user_model
from django.db import IntegrityError # Import này có thể không cần thiết ở đây nếu bạn xử lý IntegrityError ở view

User = get_user_model()

# Form để tạo Workspace mới
class WorkspaceForm(ModelForm): # Đổi tên thành WorkspaceForm cho đơn giản, hoặc giữ CreateWorkspaceForm
    class Meta:
        model = Workspace
        fields = ['name', 'thumbnail', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên Workspace'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mô tả Workspace'}),
        }

    # Có thể xóa các hàm clean_name và clean_description nếu bạn muốn sử dụng mặc định của Django
    # (Django ModelForm đã tự động kiểm tra trường required)
    # Nếu bạn muốn tùy chỉnh thông báo lỗi hoặc thêm logic phức tạp hơn thì giữ lại
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if not name:
    #         raise forms.ValidationError("Workspace name is required.")
    #     return name

    # def clean_description(self):
    #     description = self.cleaned_data.get('description')
    #     if not description:
    #         raise forms.ValidationError("Description is required.")
    #     return description


# Form để thêm thành viên mới vào workspace
class AddWorkspaceMemberForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label="Tên người dùng",
        help_text="Nhập tên người dùng muốn thêm vào workspace này."
    )

    class Meta:
        model = WorkspaceMember
        fields = ['username', 'permission', 'isAdmin']
        labels = {
            'permission': 'Quyền hạn',
            'isAdmin': 'Là quản trị viên?'
        }
        widgets = {
            'permission': forms.RadioSelect(choices=[('view', 'Xem'), ('edit', 'Sửa')])
        }

    def __init__(self, *args, **kwargs):
        self.workspace = kwargs.pop('workspace', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Người dùng với tên này không tồn tại.")

        if self.workspace and WorkspaceMember.objects.filter(workspace=self.workspace, user=user, deleted_at__isnull=True).exists():
            raise forms.ValidationError("Người dùng này đã là thành viên của workspace rồi.")

        self.cleaned_data['user'] = user
        return username


# Form để chỉnh sửa quyền của thành viên hiện có
class EditWorkspaceMemberForm(forms.ModelForm):
    class Meta:
        model = WorkspaceMember
        fields = ['permission', 'isAdmin']
        labels = {
            'permission': 'Quyền hạn',
            'isAdmin': 'Là quản trị viên?'
        }
        widgets = {
            'permission': forms.RadioSelect(choices=[('view', 'Xem'), ('edit', 'Sửa')])
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data