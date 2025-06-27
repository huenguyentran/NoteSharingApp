from django.utils import timezone
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from workspaces.models import Workspace

class DeleteWorkspaceView(LoginRequiredMixin, View):
    def post(self, request, workspace_id):
        """Xóa mềm workspace (chuyển deleted_at)"""
        workspace = get_object_or_404(Workspace, pk=workspace_id, deleted_at__isnull=True)
        workspace.deleted_at = timezone.now()
        workspace.save()
        return JsonResponse({'status': 'deleted'})
