# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\forms.py
from django import forms
from .models import Workspace, WorkspaceMember # Chỉ một dấu chấm vì models.py ngang hàng # Đảm bảo import Workspace và WorkspaceMember
from django.contrib.auth import get_user_model
from django.db import IntegrityError # Import để xử lý lỗi trùng lặp nếu cần ở form (tùy chọn)

User = get_user_model() # Lấy User model hiện tại, bao gồm cả custom user model nếu có

# Form để thêm thành viên mới vào workspace
class AddWorkspaceMemberForm(forms.ModelForm):
    # Thêm trường username để người dùng nhập username của người muốn mời
    username = forms.CharField(
        max_length=150,
        label="Tên người dùng",
        help_text="Nhập tên người dùng muốn thêm vào workspace này."
    )

    class Meta:
        model = WorkspaceMember
        # Các trường mà người dùng sẽ chọn/nhập
        # Lưu ý: 'user' sẽ được gán sau khi clean_username xác định được user object
        fields = ['username', 'permission', 'isAdmin']
        labels = {
            'permission': 'Quyền hạn',
            'isAdmin': 'Là quản trị viên?'
        }
        widgets = {
            'permission': forms.RadioSelect(choices=[('view', 'Xem'), ('edit', 'Sửa')])
        }

    # Override __init__ để nhận đối tượng workspace
    def __init__(self, *args, **kwargs):
        self.workspace = kwargs.pop('workspace', None) # Lấy workspace từ kwargs
        super().__init__(*args, **kwargs)

        # Nếu bạn muốn hiển thị dropdown list người dùng, thay vì nhập username
        # self.fields['user'] = forms.ModelChoiceField(
        #     queryset=User.objects.all(), # Lọc thêm nếu cần
        #     label="Chọn người dùng",
        #     empty_label="--- Chọn một người dùng ---"
        # )
        # self.fields['user'].required = True


    # Clean method để kiểm tra username và quyền
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Người dùng với tên này không tồn tại.")

        # Kiểm tra xem người dùng đã là thành viên của workspace này chưa
        # Đảm bảo chỉ xem các thành viên chưa bị soft-deleted
        if self.workspace and WorkspaceMember.objects.filter(workspace=self.workspace, user=user, deleted_at__isnull=True).exists():
            raise forms.ValidationError("Người dùng này đã là thành viên của workspace rồi.")

        # Lưu đối tượng user vào cleaned_data để sau này ModelForm có thể dùng để tạo WorkspaceMember
        self.cleaned_data['user'] = user 
        return username

    # Bạn có thể thêm một clean tổng thể để đảm bảo quyền admin chỉ được gán bởi admin khác (tùy chọn)
    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Logic kiểm tra thêm nếu cần
    #     return cleaned_data


# Form để chỉnh sửa quyền của thành viên hiện có
class EditWorkspaceMemberForm(forms.ModelForm):
    class Meta:
        model = WorkspaceMember
        # Chỉ cho phép chỉnh sửa quyền và trạng thái admin
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
        # Thêm logic kiểm tra nếu cần, ví dụ: không thể bỏ quyền admin của chính mình
        # (Logic này thường được xử lý tốt hơn ở View để có request.user)
        return cleaned_data
    
    from django import forms
from django.forms import ModelForm
from .models import Workspace, WorkspaceMember

class CreateWorkspaceForm(ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'thumbnail', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Workspace name is required.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Description is required.")
        return description