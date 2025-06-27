from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from workspaces.models import Workspace, WorkspaceMember
from django.contrib.auth.models import User

class WorkspaceMemberView(LoginRequiredMixin, View):

    def post(self, request, workspace_id):
        """Thêm thành viên mới vào workspace"""
        user_id = request.POST.get('user_id')
        permission = request.POST.get('permission', 'view')
        is_admin = request.POST.get('isAdmin') == 'on'

        workspace = get_object_or_404(Workspace, pk=workspace_id)
        user = get_object_or_404(User, pk=user_id)

        WorkspaceMember.objects.create(
            workspace=workspace,
            user=user,
            permission=permission,
            isAdmin=is_admin
        )
        return JsonResponse({'status': 'created'})

    def put(self, request, workspace_id):
        """Cập nhật quyền hoặc isAdmin của thành viên"""
        import json
        data = json.loads(request.body)

        member_id = data.get('member_id')
        permission = data.get('permission')
        is_admin = data.get('isAdmin')

        member = get_object_or_404(WorkspaceMember, pk=member_id, workspace_id=workspace_id)
        if permission:
            member.permission = permission
        if is_admin is not None:
            member.isAdmin = is_admin
        member.save()

        return JsonResponse({'status': 'updated'})

    def delete(self, request, workspace_id):
        """Xóa thành viên khỏi workspace"""
        import json
        data = json.loads(request.body)

        member_id = data.get('member_id')
        member = get_object_or_404(WorkspaceMember, pk=member_id, workspace_id=workspace_id)
        member.delete()

        return JsonResponse({'status': 'deleted'})
