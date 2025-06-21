from django.views import View
from django.shortcuts import render, redirect
from core.views.BaseView import BaseView


from notes.forms import CreateNoteForm



class createNoteView(BaseView):
  def get(self, request):
    form = CreateNoteForm()
    return render(request, 'create_note.html', {'form': form})
  
  def post(self, request):
    form = CreateNoteForm(request.POST)
    form.instance.create_by = request.user
    if form.is_valid():
      form.save()
      return redirect('home')  
    form = CreateNoteForm()  
    return render(request, 'create_note.html', {'form': form})