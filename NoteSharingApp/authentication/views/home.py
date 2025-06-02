from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note 
from core.views import BaseView

class HomeView(BaseView, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            deleted_notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=False)
            notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=True)
            return render(request, 'home/home.html', {'notes': notes})