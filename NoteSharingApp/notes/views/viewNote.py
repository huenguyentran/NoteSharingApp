from django.views.generic import View
from django.shortcuts import render, redirect
from notes.models import Note
from core.views.BaseView import BaseView

class viewNoteView(BaseView):
  def get(self, request, note_id):
    try:
      note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
    except Note.DoesNotExist:
      return redirect('home')
    
    return render(request, 'view_note.html', {'note': note})