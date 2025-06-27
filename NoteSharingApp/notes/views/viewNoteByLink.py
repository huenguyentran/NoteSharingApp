from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseForbidden
from core.views.ErrorView import ErrorView
from notes.models import Note  
from .BaseNoteAccess import BaseNoteAccessView


# Giả sử URL là: path('note/by-link/<uuid:note_id>/', NoteByLinkView.as_view())
# Token được truyền qua query parameter: ?token=abc123


class ByLinkNoteView(View):
    def get(self, request, note_id):
        token = request.GET.get('token')
        if not token:
            return HttpResponseForbidden("Missing token")

        try:
            note = Note.objects.get(id=note_id, is_shared_via_link=True)
        except Note.DoesNotExist:
            return ErrorView(request, message = "Không tìm thấy note hoặc Note không được chia sẻ bằng link")
        
        if str(note.share_token) != str(token):
            return HttpResponseForbidden("Invalid token")

        return render(request, "note_by_link.html", {
            "note": note,
        })
    
    