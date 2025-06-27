from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from workspaces.models import Workspace, WorkspaceMember

class CreateWorkspaceView(LoginRequiredMixin, View):
    def get(self, request):
        # Tạo workspace mới
        workspace = Workspace.objects.create(
            name="New Workspace",
            description="",
        )

        # Thêm người tạo làm admin
        WorkspaceMember.objects.create(
            workspace=workspace,
            user=request.user,
            isAdmin=True,
        )

        # Chuyển hướng đến trang chỉnh sửa chi tiết workspace
        return redirect('workspace_detail', pk=workspace.pk)
