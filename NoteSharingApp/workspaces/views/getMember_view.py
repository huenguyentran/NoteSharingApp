# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\views\getMember_view.py

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model # Sử dụng get_user_model để linh hoạt hơn
from django.shortcuts import get_object_or_404 # Cần import này để lấy Workspace
from workspaces.models import Workspace, WorkspaceMember # Cần import Workspace và WorkspaceMember
# Đảm bảo import form chính xác, ví dụ:
from ..forms import AddWorkspaceMemberForm, EditWorkspaceMemberForm
User = get_user_model()

class MemberListView(LoginRequiredMixin, ListView):
    template_name = 'Member_List.html'
    context_object_name = 'members' # Context này sẽ chứa các đối tượng WorkspaceMember

    # Trong ListView, bạn thường cần một thuộc tính để lưu đối tượng Workspace
    # hoặc lấy nó lại trong get_context_data.
    # Cách tốt nhất là lưu nó vào self.workspace trong get_queryset.
    def get_queryset(self):
        # Lưu ý: Theo traceback bạn cung cấp, URL pattern của bạn sử dụng 'pk'
        # ví dụ: path('<int:pk>/members/', ...)
        # Do đó, hãy lấy tham số là 'pk', không phải 'workspace_id'
        workspace_pk_from_url = self.kwargs.get('pk')
        
        # Lấy đối tượng Workspace và lưu nó vào self để dùng trong get_context_data
        self.workspace = get_object_or_404(Workspace, pk=workspace_pk_from_url, deleted_at__isnull=True)

        # Trả về queryset của WorkspaceMember, không phải User trực tiếp,
        # vì bạn cần thông tin về quyền (permission, isAdmin) và deleted_at.
        return WorkspaceMember.objects.filter(
            workspace=self.workspace,
            deleted_at__isnull=True
        ).order_by('joined_at') # Sắp xếp theo thời gian tham gia, hoặc user__username

    def get_context_data(self, **kwargs):
        # Gọi phương thức gốc để lấy các context mặc định của ListView (bao gồm 'members')
        context = super().get_context_data(**kwargs)

        # Thêm đối tượng workspace và pk của nó vào context
        context['workspace'] = self.workspace
        context['workspace_pk'] = self.workspace.pk

        # Thêm logic để xác định người dùng hiện tại có phải admin không
        is_admin = WorkspaceMember.objects.filter(
            workspace=self.workspace,
            user=self.request.user,
            isAdmin=True,
            deleted_at__isnull=True
        ).exists()
        context['is_admin'] = is_admin

        # Thêm form để thêm thành viên mới
        context['add_member_form'] = AddWorkspaceMemberForm(workspace=self.workspace)
        
        # Thêm ID của người dùng hiện tại để xử lý logic hiển thị nút trên frontend
        context['current_user_id'] = self.request.user.id

        return context