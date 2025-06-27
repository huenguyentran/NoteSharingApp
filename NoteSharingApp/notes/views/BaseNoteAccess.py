from django.http import Http404, HttpResponseForbidden
from django.views import View
from notes.models import Note

# Quyền truy cập: view, edit, owner
# Lớp cha -> các view khác sẽ kế thừa từ lớp này
# Các lớp con kế thừa lớp này: ShareNote, EditNote, DeleteNote, GetNote


class BaseNoteAccessView(View):
    permission_required = None  # Quyền truy cập yêu cầu để thực hiện thao tác: owner, view, edit
    require_login = True        # nếu False thì cho phép truy cập không đăng nhập (share link)

    def get_note(self, **kwargs):
        raise NotImplementedError("Bạn phải implement phương thức get_note")

    def get_permission(self, note, user, token=None):
        return note.get_permission(user=user, token=token)

    #kiểm tra quyền truy cập ghi chú của user với note
    def has_permission(self, note, user, token=None):
        if note.workspace:
            # Ghi chú thuộc workspace → lấy quyền từ workspace
            member = note.workspace.members.filter(user=user).first()
            if not member:
                return None
            if member.isAdmin:
                return 'owner'
            return member.permission

        perm = self.get_permission(note, user, token)
        if self.permission_required == 'owner':
            return perm == 'owner'
        if self.permission_required == 'edit':
            return perm in ['edit', 'owner']
        if self.permission_required == 'view':
            return perm in ['view', 'edit', 'owner']
        return False


    #Override lại để kiểm tra người dùng có quyền với Note không
    def dispatch(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        token = kwargs.get("token")
        try:
            note = self.get_note(**kwargs)
        except Note.DoesNotExist:
            raise Http404("Note không tồn tại.")

        if self.require_login and not user:
            return HttpResponseForbidden("Cần đăng nhập để truy cập.")

        if not self.has_permission(note, user, token):
            return HttpResponseForbidden("Bạn không có quyền truy cập ghi chú này.")

        self.note = note
        self.permission = note.get_permission(user, token)
        return super().dispatch(request, *args, **kwargs)