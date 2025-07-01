# NoteSharingApp/workspaces/views/getNotesWorkspace_View.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from notes.models import Note
from workspaces.models import Workspace # Cần import Workspace để lọc theo members

class GetNotesWorkspaceView(LoginRequiredMixin, ListView): # Đảm bảo tên lớp này trùng với tên lớp trong file của bạn
    model = Note
    template_name = 'Note_List.html'
    context_object_name = 'notes'

    def get_queryset(self):
        # Lấy PK của workspace từ URL, được truyền qua kwargs['pk']
        workspace_pk = self.kwargs['pk'] # <-- THAY ĐỔI TỪ 'workspace_id' SANG 'pk'
        
        # Lọc các ghi chú thuộc về workspace này VÀ người dùng hiện tại là thành viên của workspace đó
        try:
            # Kiểm tra xem workspace có tồn tại và người dùng hiện tại có phải là thành viên không
            workspace = Workspace.objects.get(pk=workspace_pk, members__user=self.request.user)
            # Lấy tất cả các note trong workspace này (và chưa bị xóa mềm nếu có)
            # Giả sử bạn có trường deleted_at trong Note, nếu không thì bỏ phần `deleted_at__isnull=True`
            queryset = Note.objects.filter(workspace=workspace, deleted_at__isnull=True).order_by('-created_at')
            return queryset
        except Workspace.DoesNotExist:
            # Nếu workspace không tồn tại hoặc người dùng không phải là thành viên hợp lệ, trả về QuerySet rỗng
            return Note.objects.none()