from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from notes.models import Note
from workspaces.models import WorkspaceFile

class FileWorkspaceListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'File_List.html'
    context_object_name = 'files'

    def get_queryset(self):
        workspace_id = self.kwargs.get('workspace_id')
        return WorkspaceFile.objects.filter(workspace__id=workspace_id)