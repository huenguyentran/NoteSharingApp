# notes/views/createNote.py
from django.views import View
from django.shortcuts import render, redirect
from core.views.BaseView import BaseView # Đảm bảo BaseView của bạn được import đúng

from notes.models import Note
from notes.forms.createNoteForm import CreateNoteForm
from workspaces.models import Workspace
from django.shortcuts import render, redirect, get_object_or_404 # <--- THÊM get_object_or_404
from django.urls import reverse # <--- THÊM reverse


class createNoteView(BaseView):
    def get(self, request):
        # Tạo một form trống để hiển thị khi người dùng truy cập trang tạo ghi chú
        form = CreateNoteForm()
        return render(request, 'create_note.html', {'form': form})

    def post(self, request):
        form = CreateNoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.create_by = request.user 

            # Lấy workspace_id từ query parameters (từ URL: ?workspace_id=...)
            workspace_id = request.GET.get('workspace_id')

            redirect_url = 'dashboard' # Mặc định sẽ chuyển hướng về dashboard

            if workspace_id:
                try:
                    # Lấy workspace và kiểm tra quyền của người dùng
                    # Đảm bảo người dùng hiện tại là thành viên của workspace đó
                    workspace = get_object_or_404(Workspace, pk=workspace_id, members__user=request.user)
                    note.workspace = workspace # Gán ghi chú vào workspace này
                    # Nếu thành công, chuyển hướng về trang chi tiết workspace
                    redirect_url = reverse('workspace_detail', kwargs={'pk': workspace.pk})
                except Exception as e:
                    # Ghi log lỗi hoặc xử lý khác nếu workspace không tìm thấy/không có quyền
                    print(f"Lỗi khi gán ghi chú vào workspace (ID: {workspace_id}): {e}")
                    # Bạn có thể thêm message cảnh báo cho người dùng ở đây nếu muốn

            note.save() # Lưu ghi chú sau khi đã gán workspace (nếu có)

            return redirect(redirect_url) # Chuyển hướng đến URL đã xác định

        return render(request, 'create_note.html', {'form': form})