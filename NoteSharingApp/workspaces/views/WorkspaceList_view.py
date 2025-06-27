from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from workspaces.models import Workspace


#Trả về danh sách workspace của người dùng hiện tại
class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    template_name = 'Workspace_List.html'
    context_object_name = 'workspaces'

    def get_queryset(self):
        return Workspace.objects.filter(members__user=self.request.user).distinct()
