# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\notes\views\deleteNote.py
from django.http import JsonResponse, Http404 # Đảm bảo Http404 được import
from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic import View # Không cần View ở đây vì bạn kế thừa BaseNoteAccessView
from notes.views.BaseNoteAccess import BaseNoteAccessView
from core.views import ErrorView # Nếu bạn sử dụng ErrorView để xử lý lỗi
from notes.models import Note
from django.utils import timezone
from django.urls import reverse # Import reverse để chuyển hướng

class deleteNoteView(BaseNoteAccessView): 
    # Sửa dấu phẩy thừa: từ 'owner', thành 'owner' (chuỗi) hoặc ('owner',) (tuple rõ ràng)
    permission_required = 'owner' 
    require_login = True

    # === PHƯƠNG THỨC MỚI CẦN THÊM ===
    # Implement phương thức get_note mà BaseNoteAccessView yêu cầu
    def get_note(self, **kwargs):
        note_id = kwargs.get('note_id')
        if not note_id:
            raise Http404("Không tìm thấy note_id trong URL.")
        # Lấy ghi chú, bao gồm cả những ghi chú đã bị xóa mềm nếu cần cho các view khác,
        # nhưng ở đây ta chỉ xóa (mềm), nên không cần quan tâm deleted_at.
        return get_object_or_404(Note, pk=note_id)

    # === Cập nhật phương thức post ===
    def post(self, request, note_id):
        if self.note.deleted_at:
            # Nếu ghi chú đã bị xóa, chuyển hướng về dashboard hoặc trang thông báo lỗi
            # Thay vì JsonResponse vì đây là POST từ form
            messages.error(request, 'Ghi chú này đã bị xóa rồi.')
            return redirect(reverse('dashboard')) # Chuyển hướng về dashboard

        try:
            self.note.deleted_at = timezone.now()
            self.note.save()
            # Thêm thông báo thành công (tùy chọn)
            from django.contrib import messages
            messages.success(request, 'Ghi chú đã được xóa thành công.')
            # CHUYỂN HƯỚNG SAU KHI XÓA THÀNH CÔNG
            return redirect(reverse('dashboard')) # Hoặc 'note_list' tùy ý bạn

        except Exception as e:
            print(f"Lỗi khi xóa ghi chú: {e}")
            # Thêm thông báo lỗi
            from django.contrib import messages
            messages.error(request, f'Lỗi khi xóa ghi chú: {e}')
            # Chuyển hướng về trang trước đó hoặc dashboard
            return redirect(request.META.get('HTTP_REFERER', reverse('dashboard')))
    def get(self, request, note_id):
        # Trong trường hợp này, nếu ai đó cố gắng truy cập URL /notes/delete/<note_id>/ bằng GET
        # chúng ta sẽ chuyển hướng họ về trang chi tiết workspace của ghi chú đó.
        # self.note đã có sẵn nhờ BaseNoteAccessView.dispatch
        if hasattr(self, 'note') and self.note.workspace:
            return redirect(reverse('workspace_detail', kwargs={'pk': self.note.workspace.pk}))
        else:
            # Nếu không tìm thấy workspace hoặc note, có thể chuyển hướng về dashboard
            # hoặc hiển thị trang lỗi.
            return redirect(reverse('dashboard')) # Thay 'dashboard' bằng tên URL dashboard của bạn
            # Hoặc raise Http404("Trang không tồn tại hoặc không có quyền truy cập.")