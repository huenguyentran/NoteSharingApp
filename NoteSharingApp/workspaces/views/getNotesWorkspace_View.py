from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from notes.models import Note
from workspaces.models import Workspace

class NoteWorkspaceListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'Note_List.html'
    context_object_name = 'notes'

    def get_queryset(self):
        workspace_id = self.kwargs.get('workspace_id')
        return Note.objects.filter(workspace__id=workspace_id)