# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\views\deleteWorkspace_View.py

from django.utils import timezone
from django.views import View # Hoặc DeleteView nếu bạn muốn dùng generic view
from django.http import JsonResponse, HttpResponseRedirect # Cần HttpResponseRedirect nếu dùng soft delete với DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Workspace, WorkspaceMember # Import Workspace và WorkspaceMember

class DeleteWorkspaceView(LoginRequiredMixin, View): # Giữ nguyên View nếu bạn muốn tự xử lý hoàn toàn
    def post(self, request, pk): # <--- Đổi workspace_id thành pk
        # Đảm bảo workspace tồn tại và chưa bị xóa mềm
        workspace = get_object_or_404(Workspace, pk=pk, deleted_at__isnull=True)
        
        # Thêm kiểm tra quyền ở đây (rất quan trọng)
        # Chỉ chủ sở hữu hoặc admin của workspace mới có quyền xóa
        if request.user != workspace.owner and not WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user,
            isAdmin=True,
            deleted_at__isnull=True
        ).exists():
            return JsonResponse({'status': 'error', 'message': 'Bạn không có quyền xóa workspace này.'}, status=403)

        workspace.deleted_at = timezone.now() # Xóa mềm
        workspace.save()
        
        # Nếu đây là AJAX request, JsonResponse là hợp lý
        return JsonResponse({'status': 'success', 'message': 'Workspace đã được xóa thành công.'})

        # Nếu bạn muốn chuyển hướng sau khi xóa (ví dụ, nếu không phải AJAX)
        # return HttpResponseRedirect(reverse_lazy('workspace_list')) # Cần import reverse_lazy