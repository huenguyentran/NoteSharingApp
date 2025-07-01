from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from notes.models import Note, NoteShare # Đã sửa: Import NoteShare
from core.views.BaseView import BaseView

class viewNoteView(BaseView):
    def get(self, request, note_id):
        # 1. Thử tìm ghi chú thuộc sở hữu của người dùng hiện tại
        try:
            note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
        except Note.DoesNotExist:
            # 2. Nếu không tìm thấy, thử tìm trong các ghi chú được chia sẻ với người dùng hiện tại
            #    Dùng NoteShare model và kiểm tra recipient (share_with)
            shared_note_entry = NoteShare.objects.filter(
                share_with=request.user, 
                note__id=note_id, # Truy cập ID của Note thông qua mối quan hệ 'note'
                note__deleted_at__isnull=True # Đảm bảo ghi chú gốc không bị xóa
            ).first() 

            if shared_note_entry:
                note = shared_note_entry.note # Lấy đối tượng Note từ bản ghi chia sẻ
            else:
                # 3. Nếu không tìm thấy trong cả hai trường hợp, chuyển hướng về dashboard
                return redirect('dashboard') 
        
        return render(request, 'view_note.html', {'note': note})