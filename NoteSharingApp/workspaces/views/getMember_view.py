from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from workspaces.models import Workspace

class MemberListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'Member_List.html'
    context_object_name = 'members'

    def get_queryset(self):
        workspace_id = self.kwargs.get('workspace_id')
        return User.objects.filter(workspace_memberships__workspace__id=workspace_id).distinct()
