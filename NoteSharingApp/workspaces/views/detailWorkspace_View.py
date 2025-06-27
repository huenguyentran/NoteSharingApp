from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView
from workspaces.models import Workspace

class DetailWorkspaceView(LoginRequiredMixin, DetailView):
    model = Workspace
    template_name = 'Workspace_Detail.html'
    context_object_name = 'workspace'

    #Giới hạn truy cập, chỉ chọn các wp có người dùng
    def get_queryset(self):
        return Workspace.objects.filter(members__user=self.request.user)
