from django.views import View
from django.http import JsonResponse, Http404, HttpResponseForbidden
from NoteSharingApp.notes.models import Note  
from .BaseNoteAccess import BaseNoteAccessView


# Giả sử URL là: path('note/by-link/<uuid:note_id>/', NoteByLinkView.as_view())
# Token được truyền qua query parameter: ?token=abc123


class ByLinkNoteView(BaseNoteAccessView):
    permission_required = 'view'
    require_login = False
    #Cho phép truy cập ko yêu cầu login, yêu cầu token

    def get_note(self, **kwargs):
        note_id = kwargs.get('note_id')
        return Note.objects.get(id=note_id)

    def get(self, request, *args, **kwargs):
        note = self.note  # Đã được gán bởi dispatch
        data = {
            'id': str(note.id),
            'title': note.title,
            'content': note.content,
            'permission': self.permission
        }
        return JsonResponse(data)