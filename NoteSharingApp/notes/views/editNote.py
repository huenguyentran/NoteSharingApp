from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect 
from notes.models import Note, NoteShare
from notes.forms import EditNoteForm
from core.views.BaseView import BaseView

from core.views.ErrorView import ErrorView

class editNoteView(BaseView):
  def get(self, request, note_id):
    try:
      note = request.user.notes.get(id=note_id, deleted_at__isnull=True)

    except Note.DoesNotExist:
      return ErrorView(request, "Không tìm thấy ghi chú!", status=404)
    
    
    form = EditNoteForm(instance=note)

    user = request.user
    share = NoteShare.objects.filter(note=note, share_with=user).first()
    if (share and share.permission == 'edit') or (note.create_by == user):
      return render(request, 'edit_note.html', {'form': form, 'note': note})
    
    else:
      return redirect('view_note', note_id=note.id)
    


  def post(self, request, note_id):
    try:
      note = request.user.notes.get(id=note_id, deleted_at__isnull=True)

    except Note.DoesNotExist:
      return HttpResponse("Lỗi ko tìm thấy note!")
    
    share = NoteShare.objects.filter(note=note, share_with=request.user).first()
    if (share and share.permission == 'view') or share is None:
        return HttpResponse("Bạn không có quyền chỉnh sửa ghi chú này.")

    form = EditNoteForm(request.POST, instance=note) 
    if form.is_valid():
      form.save()
      return redirect('home')
    return render(request, 'edit_note.html', {'form': form, 'note': note})