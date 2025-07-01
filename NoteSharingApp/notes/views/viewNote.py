# notes/views/viewNote.py
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from notes.models import Note, NoteShare 
from core.views.BaseView import BaseView

class viewNoteView(BaseView):
    def get(self, request, note_id):
        note = None
        permission = None
        is_shared_to_current_user = False # Biến mới để xác định nếu ghi chú được chia sẻ tới người dùng hiện tại

        # 1. Thử tìm ghi chú thuộc sở hữu của người dùng hiện tại
        try:
            note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
            permission = 'owner' # Người sở hữu luôn có quyền 'owner'
        except Note.DoesNotExist:
            # 2. Nếu không tìm thấy, thử tìm trong các ghi chú được chia sẻ với người dùng hiện tại
            shared_note_entry = NoteShare.objects.filter(
                share_with=request.user, 
                note__id=note_id, 
                note__deleted_at__isnull=True
            ).first() 

            if shared_note_entry:
                note = shared_note_entry.note
                permission = shared_note_entry.permission # Lấy quyền từ đối tượng NoteShare
                is_shared_to_current_user = True # Đánh dấu đây là ghi chú được chia sẻ
            else:
                # 3. Nếu không tìm thấy trong cả hai trường hợp, thử tìm ghi chú được chia sẻ qua link (nếu có token trong request)
                # Lưu ý: Logic này có thể đã được xử lý bởi một view khác (ví dụ: viewNoteByLink)
                # Nhưng để đảm bảo, chúng ta có thể kiểm tra ở đây nếu bạn muốn viewNote cũng xử lý link share.
                # Tuy nhiên, thông thường view NoteByLink sẽ có logic riêng và không cần lặp lại ở đây.
                # Do yêu cầu chỉ liên quan đến quyền của user đăng nhập, nên không cần token ở đây.
                return redirect('dashboard') 
        
        if note:
            context = {
                'note': note,
                'permission': permission,
                'is_shared_to_current_user': is_shared_to_current_user,
                'is_owner': (note.create_by == request.user), # Thêm biến này để kiểm tra chủ sở hữu trong template
            }
            return render(request, 'view_note.html', context)
        else:
            return redirect('dashboard')