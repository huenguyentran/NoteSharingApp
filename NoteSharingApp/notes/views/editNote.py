from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect 
from .BaseNoteAccess import BaseNoteAccessView
from notes.models import Note, NoteShare
from notes.forms import EditNoteForm
from core.views.BaseView import BaseView

from core.views.ErrorView import ErrorView

class editNoteView(BaseNoteAccessView):
    permission_required = 'edit'
    require_login = True

    def get_note(self, note_id):
        return Note.objects.get(pk=note_id)
    
    def get(self, request, note_id):
        # BaseNoteAccessView đã gán self.note
        # Nếu self.note không tồn tại do lỗi truy cập (ErrorView đã xử lý), hàm này sẽ không được gọi
        
        form = EditNoteForm(instance=self.note)
        
        # Lấy link chia sẻ nếu ghi chú đang được chia sẻ qua link
        share_link = None
        if self.note.is_shared_via_link:
            share_link = self.note.get_share_link()

        return render(request, 'edit_note.html', {
            'form': form, 
            'note': self.note,
            'share_link': share_link, # Truyền share_link vào context
        })
    
    def post(self, request, note_id):
        # BaseNoteAccessView đã gán self.note
        # Nếu self.note không tồn tại do lỗi truy cập (ErrorView đã xử lý), hàm này sẽ không được gọi

        form = EditNoteForm(request.POST, instance=self.note) 
        
        if form.is_valid():
            # Lấy giá trị hiện tại của is_shared_via_link trước khi lưu form
            old_is_shared_via_link = self.note.is_shared_via_link
            
            # Lưu form trước để cập nhật các trường như title, content, is_shared_via_link, link_permission
            note = form.save(commit=False) # Không commit ngay để có thể thay đổi thêm

            # Xử lý logic chia sẻ qua link
            if note.is_shared_via_link and not old_is_shared_via_link:
                # Nếu người dùng vừa bật chia sẻ link (trước đó là false, giờ là true)
                # Đảm bảo token được tạo mới (mặc dù default=uuid.uuid4 đã làm điều này)
                # Và quyền được thiết lập theo form
                if not note.share_token: # Đảm bảo có token nếu chưa có (ví dụ: migrate từ bản cũ)
                    note.share_token = uuid.uuid4()
                # link_permission đã được cập nhật qua form.save()
                
            elif not note.is_shared_via_link and old_is_shared_via_link:
                # Nếu người dùng vừa tắt chia sẻ link (trước đó là true, giờ là false)
                # Đặt lại share_token về giá trị mặc định hoặc None nếu bạn muốn
                # Django's UUIDField với default=uuid.uuid4 sẽ tự tạo khi object mới.
                # Để hủy bỏ token cũ, bạn có thể tạo token mới hoặc đặt None/null nếu trường cho phép.
                # Ở đây ta giữ nguyên token nhưng chỉ dựa vào is_shared_via_link để kiểm soát.
                pass # Không cần làm gì nhiều, is_shared_via_link = False đã đủ

            note.save() # Lưu các thay đổi vào database

            # Lấy lại link chia sẻ sau khi đã lưu note
            share_link = None
            if note.is_shared_via_link:
                share_link = note.get_share_link()
            
            # Có thể chuyển hướng về trang xem chi tiết ghi chú thay vì dashboard để người dùng kiểm tra
            return redirect('view_note', note_id=note.id) # Giả định bạn có URL 'view_note'
        
        # Nếu form không hợp lệ, render lại trang với lỗi và share_link hiện có (nếu có)
        share_link = self.note.get_share_link() if self.note.is_shared_via_link else None
        return render(request, 'edit_note.html', {
            'form': form, 
            'note': self.note,
            'share_link': share_link,
        })