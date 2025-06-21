from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note 
from .BaseView import BaseView

# Dashboard: NoteList (Da xóa/ chưa xóa) + Danh sách Workspace(mhoms...) + User Infor + User Friend (nếu làm kịp)
# Có thể làm DashBoard riêng cho chưa đăng nhập

class DashBoardView(BaseView, View):
    def get(self, request):

        deleted_notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=False)
        notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=True)
        return render(request, 'dashboard/dashboard.html', {'notes': notes})