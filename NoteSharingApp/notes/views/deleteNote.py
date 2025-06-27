from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from notes.views.BaseNoteAccess import BaseNoteAccessView
from core.views import ErrorView
from notes.models import Note

from django.utils import timezone

class deleteNoteView(BaseNoteAccessView): 
    permission_required = 'owner',
    require_login = True


    def post(self, request, note_id):
        self.note.deleted_at = timezone.now()
        self.note.save()
        return JsonResponse({'success': True})
