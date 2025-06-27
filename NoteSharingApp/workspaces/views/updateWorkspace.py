from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from workspaces.models import Workspace

class UpdateWorkspaceView(LoginRequiredMixin, View):
    def get(self, request, workspace_id):
        """Hiển thị form cập nhật"""
        workspace = get_object_or_404(Workspace, pk=workspace_id, deleted_at__isnull=True)
        return render(request, 'workspace_form.html', {'workspace': workspace})

    def post(self, request, workspace_id):
        """Xử lý cập nhật"""
        workspace = get_object_or_404(Workspace, pk=workspace_id, deleted_at__isnull=True)
        workspace.name = request.POST.get('name', workspace.name)
        workspace.description = request.POST.get('description', workspace.description)
        if request.FILES.get('thumbnail'):
            workspace.thumbnail = request.FILES['thumbnail']
        workspace.save()
        return redirect('workspace_detail', pk=workspace.id)
