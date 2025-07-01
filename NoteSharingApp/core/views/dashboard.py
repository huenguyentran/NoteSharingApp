from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note, NoteShare

from .BaseView import BaseView

# Dashboard: NoteList (Da xóa/ chưa xóa) + Danh sách Workspace(mhoms...) + User Infor + User Friend (nếu làm kịp)
# Có thể làm DashBoard riêng cho chưa đăng nhập

#Trang Dashboard: ....

class DashBoardView(BaseView, View):
    def get(self, request):
        notes = Note.objects.filter(create_by=request.user, deleted_at__isnull=True)
        # Ghi chú được người khác chia sẻ
        shared_notes = NoteShare.objects.filter(
            share_with=request.user,
            note__deleted_at__isnull=True
        ).select_related('note', 'share_by')

        return render(request, 'dashboard/dashboard.html', {
            'notes': notes,
            'shared_notes': shared_notes
        })