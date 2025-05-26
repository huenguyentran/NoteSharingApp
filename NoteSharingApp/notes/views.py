from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import NoteForm

def index(request):
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