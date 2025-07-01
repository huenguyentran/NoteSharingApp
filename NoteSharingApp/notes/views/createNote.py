# notes/views/createNote.py
from django.views import View
from django.shortcuts import render, redirect
from core.views.BaseView import BaseView # Đảm bảo BaseView của bạn được import đúng

from notes.models import Note
from notes.forms.createNoteForm import CreateNoteForm


class createNoteView(BaseView):
    def get(self, request):
        # Tạo một form trống để hiển thị khi người dùng truy cập trang tạo ghi chú
        form = CreateNoteForm()
        return render(request, 'create_note.html', {'form': form})

    def post(self, request):
        # Khởi tạo form với dữ liệu POST
        form = CreateNoteForm(request.POST)

        # Kiểm tra tính hợp lệ của form
        if form.is_valid():
            # Lưu form nhưng không commit vào CSDL ngay lập tức (commit=False)
            # Điều này cho phép chúng ta gán thêm các thuộc tính cho đối tượng Note trước khi lưu
            note = form.save(commit=False)
            
            # Gán người dùng hiện tại (người tạo ghi chú) vào trường 'create_by'
            # Giả sử trường 'create_by' trong Note model của bạn là một ForeignKey tới User model
            note.create_by = request.user 
            
            # Lưu đối tượng Note đã hoàn chỉnh vào cơ sở dữ liệu
            note.save()
            
            # Chuyển hướng người dùng đến trang dashboard sau khi tạo ghi chú thành công
            # Đảm bảo bạn có một URL với tên 'dashboard' được cấu hình
            return redirect('dashboard')
        
        # Nếu form không hợp lệ, hiển thị lại trang tạo ghi chú với các lỗi form
        # Form sẽ tự động chứa thông tin đã nhập và lỗi tương ứng
        return render(request, 'create_note.html', {'form': form})