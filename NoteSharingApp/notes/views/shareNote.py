from django.views import View
from core.views.BaseView import BaseView
# from notes.views.BaseNoteAccess import BaseNoteAccessView # Not used directly in this snippet
from core.views.ErrorView import ErrorView # Make sure ErrorView returns an HttpResponse
from notes.models import NoteShare, Note
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.mixins import LoginRequiredMixin # Not used directly in this snippet
from django.contrib.auth.models import User
import uuid # Needed for note.share_token, make sure it's imported if used.

class shareNoteView(BaseView):
    template_name = 'notes/share_note.html' # Đảm bảo đường dẫn template chính xác

    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id, create_by=request.user) # Thêm create_by để đảm bảo chỉ chủ sở hữu có thể xem trang chia sẻ

        # Không cần kiểm tra if note.create_by != request.user: ở đây nữa
        # vì get_object_or_404 đã bao gồm điều kiện này.
        # Nếu người dùng không phải chủ sở hữu, get_object_or_404 sẽ tự động raise 404
        # hoặc bạn có thể muốn redirect về dashboard/error page.
        # Hiện tại, tôi sẽ giả định BaseView hoặc middleware của bạn xử lý auth,
        # và get_object_or_404 là đủ cho quyền sở hữu.
        # Nếu muốn redirect thay vì 404, bạn có thể dùng filter().first() và kiểm tra None.
        
        # Lấy danh sách những người đã được chia sẻ ghi chú này
        shared_users = NoteShare.objects.filter(note=note).select_related('share_with')
        
        # Lấy tất cả người dùng trừ người hiện tại và những người đã được chia sẻ note này
        existing_share_user_ids = shared_users.values_list('share_with__id', flat=True)
        available_users = User.objects.exclude(id=request.user.id).exclude(id__in=existing_share_user_ids)

        return render(request, self.template_name, {
            'note': note,
            'users': available_users, # Truyền available_users
            'shared_users': shared_users,
            'share_link': note.get_share_link() if note.is_shared_via_link else None # Đảm bảo method get_share_link() tồn tại
        })
    

    def post(self, request, note_id):
        # Kiểm tra quyền sở hữu ngay từ đầu
        note = get_object_or_404(Note, id=note_id, create_by=request.user)
        # Nếu bạn muốn trả về một ErrorView thay vì 404 của get_object_or_404, bạn có thể làm như sau:
        # try:
        #     note = Note.objects.get(id=note_id, create_by=request.user)
        # except Note.DoesNotExist:
        #     return ErrorView(request, "Bạn không có quyền chia sẻ ghi chú này", status=403) # 403 Forbidden

        success_message = None
        error_message = None

        if 'share_with_ids' in request.POST:
            share_with_ids = request.POST.getlist('share_with_ids')
            permission = request.POST.get('permission')

            if not permission in ['view', 'edit']:
                error_message = "Quyền không hợp lệ."
            elif not share_with_ids:
                error_message = "Vui lòng chọn người dùng để chia sẻ."
            else:
                users_shared_names = []
                for uid in share_with_ids:
                    try:
                        user = User.objects.get(id=uid)
                        NoteShare.objects.update_or_create(
                            note=note,
                            share_by=request.user, # Người chia sẻ là người dùng hiện tại
                            share_with=user,
                            defaults={'permission': permission}
                        )
                        users_shared_names.append(user.username)
                    except User.DoesNotExist:
                        # Log this or add to a list of failed shares if necessary
                        continue 
                if users_shared_names:
                    success_message = f"Đã chia sẻ ghi chú với: {', '.join(users_shared_names)}."
                else:
                    error_message = "Không có người dùng nào được chia sẻ thành công."
            
        elif 'update_permissions' in request.POST:
            # Lặp qua tất cả các chia sẻ hiện có của note này để cập nhật
            shares_to_update = NoteShare.objects.filter(note=note)
            updated_count = 0
            for share in shares_to_update:
                new_perm = request.POST.get(f'permission_{share.id}') # Đảm bảo tên trường trong form khớp
                if new_perm in ['view', 'edit'] and share.permission != new_perm:
                    share.permission = new_perm
                    share.save()
                    updated_count += 1
            if updated_count > 0:
                success_message = f"Đã cập nhật {updated_count} quyền chia sẻ."
            else:
                error_message = "Không có quyền nào được cập nhật."
            # LƯU Ý QUAN TRỌNG: Lệnh return phải nằm NGOÀI vòng lặp for
            # Nếu không, nó sẽ redirect ngay sau khi xử lý phần tử đầu tiên
            # Đây chính là lỗi logic có thể đã gây ra 'return None' nếu vòng lặp trống

        elif 'delete_share_id' in request.POST: 
            share_id = request.POST.get('delete_share_id')
            try:
                # Đảm bảo người dùng hiện tại là chủ sở hữu note và chia sẻ thuộc note đó
                share = NoteShare.objects.get(id=share_id, note=note)
                share.delete()
                success_message = "Hủy chia sẻ thành công!"
            except NoteShare.DoesNotExist:
                error_message = "Hủy chia sẻ không thành công hoặc không tìm thấy chia sẻ."
        
        elif 'enable_link_sharing' in request.POST:
            link_permission = request.POST.get('link_permission', 'view')
            try:
                note.enable_share_link(link_permission) # Make sure this method exists and handles save()
                success_message = "Đã kích hoạt chia sẻ qua liên kết!"
            except ValueError as e:
                error_message = str(e) # Catch validation errors from enable_share_link

        elif 'disable_link_sharing' in request.POST:
            note.is_shared_via_link = False
            note.share_token = uuid.uuid4() # Reset token for security
            note.save()
            success_message = "Đã vô hiệu hóa chia sẻ qua liên kết."
        
        # Luôn luôn render lại trang hoặc redirect ở cuối phương thức post
        # để đảm bảo một HttpResponse được trả về.
        # Cập nhật lại các biến context sau khi POST request được xử lý
        shared_users = NoteShare.objects.filter(note=note).select_related('share_with')
        existing_share_user_ids = shared_users.values_list('share_with__id', flat=True)
        available_users = User.objects.exclude(id=request.user.id).exclude(id__in=existing_share_user_ids)

        context = {
            'note': note,
            'users': available_users,
            'shared_users': shared_users,
            'success': success_message,
            'error': error_message,
            'share_link': note.get_share_link() if note.is_shared_via_link else None
        }
        return render(request, self.template_name, context)