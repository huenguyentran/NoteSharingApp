from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from workspaces.models import Workspace, WorkspaceFile


class WorkspaceFileView(LoginRequiredMixin, View):
    def post(self, request, workspace_id):
        """Tải lên file mới"""
        workspace = get_object_or_404(Workspace, pk=workspace_id)
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return HttpResponseBadRequest("Không có file được chọn.")

        WorkspaceFile.objects.create(
            workspace=workspace,
            file=uploaded_file,
            uploaded_by=request.user
        )
        return JsonResponse({'status': 'uploaded'})
    
    def delete(self, request, workspace_id):
        """Xóa file - dùng JS gọi bằng fetch (method: DELETE)"""
        import json
        data = json.loads(request.body)
        file_id = data.get('file_id')

        file = get_object_or_404(WorkspaceFile, pk=file_id, workspace_id=workspace_id)

        # Chỉ người upload mới được xóa
        if file.uploaded_by != request.user:
            return HttpResponseForbidden("Bạn không có quyền xóa file này.")

        file.delete()
        return JsonResponse({'status': 'deleted'})
