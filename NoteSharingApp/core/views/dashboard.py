from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note 
from .BaseView import BaseView

class DashBoardView(BaseView, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            deleted_notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=False)
            notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=True)
            return render(request, 'dashboard/dashboard.html', {'notes': notes})