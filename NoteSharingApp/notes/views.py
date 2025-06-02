from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render

from notes.models import Note

from .forms import NoteForm

def index_note(request):
    return HttpResponse("Hello, world.")

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        form.instance.create_by = request.user
        if form.is_valid():
            form.save()
            return HttpResponse("✅ Note saved successfully!")  
    else:
        form = NoteForm()
    return render(request, 'create_note.html', {'form': form})

def edit_note(request, note_id):
    try:
        note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
    except Note.DoesNotExist:
        return HttpResponse("Note not found or you do not have permission to edit it.", status=404)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponse("✅ Note updated successfully!")
    else:
        form = NoteForm(instance=note)

    return render(request, 'edit_note.html', {'form': form, 'note': note})

def delete_note(request, note_id):
    try:
        note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
    except Note.DoesNotExist:
        return HttpResponse("Note not found or you do not have permission to delete it.", status=404)

    note.deleted_at = timezone.now()
    note.save()
    return HttpResponse("Note deleted successfully!")

def view_note(request, note_id):
    try:
        note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
    except Note.DoesNotExist:
        return HttpResponse("Note not found or you do not have permission to view it.", status=404)

    return render(request, 'view_note.html', {'note': note})