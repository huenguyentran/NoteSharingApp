# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\views\createWorkspace_View.py

from django.views.generic.edit import CreateView # Thay thế 'View' bằng 'CreateView'
from django.urls import reverse_lazy # Import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Workspace, WorkspaceMember # Import các model cần thiết
from ..forms import WorkspaceForm # Import form WorkspaceForm mà bạn đã sửa trong forms.py

class CreateWorkspaceView(LoginRequiredMixin, CreateView):
    model = Workspace
    form_class = WorkspaceForm # Gán form bạn đã định nghĩa
    template_name = 'create_workspace.html'
    success_url = reverse_lazy('workspace_list') # URL để chuyển hướng sau khi tạo thành công

    def form_valid(self, form):
        # Phương thức này được gọi khi form được POST và dữ liệu hợp lệ.
        # Gán người dùng hiện tại làm chủ sở hữu (owner) của workspace trước khi lưu.
        form.instance.owner = self.request.user
        
        # Lưu workspace vào database. 'super().form_valid(form)' sẽ thực hiện việc này
        # và trả về một HttpResponseRedirect.
        response = super().form_valid(form) 

        # Sau khi workspace được tạo và lưu (self.object là đối tượng Workspace vừa tạo),
        # thêm người tạo làm thành viên admin của workspace đó.
        WorkspaceMember.objects.create(
            workspace=self.object, # self.object là đối tượng Workspace vừa được lưu
            user=self.request.user,
            isAdmin=True,
            permission='edit' # Gán quyền 'edit' cho chủ sở hữu
        )
        return response

    # KHÔNG CẦN định nghĩa lại phương thức get() ở đây.
    # CreateView sẽ tự động xử lý việc hiển thị form trống trên GET request.