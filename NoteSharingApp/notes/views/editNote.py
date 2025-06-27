from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect 
from .BaseNoteAccess import BaseNoteAccessView
from notes.models import Note, NoteShare
from notes.forms import EditNoteForm
from core.views.BaseView import BaseView

from core.views.ErrorView import ErrorView

class editNoteView(BaseNoteAccessView):
  permission_required = 'edit'
  require_login = True

  def get_note(self, note_id):
    return Note.objects.get(pk = note_id)
  

  def get(self, request, note_id):
  
    form = EditNoteForm(instance=self.note)

    user = request.user
    share = NoteShare.objects.filter(note=self.note, share_with=user).first()
    share_link = self.note.get_share_link() if self.note.is_shared_via_link else None
    return render(request, 'edit_note.html', {
      'form': form, 
      'note': self.note,
      'share_link': share_link,
    })
    


  def post(self, request, note_id):
    form = EditNoteForm(request.POST, instance=self.note) 
    if form.is_valid():
      form.save()
      return redirect('note_main')
    return render(request, 'edit_note.html', {'form': form, 'note': self.note})