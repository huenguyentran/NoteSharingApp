# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\views\workspaceMembers.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import JsonResponse, Http404
from django.db import IntegrityError # Để xử lý unique_together

from ..models import Workspace, WorkspaceMember # Import Workspace và WorkspaceMember từ models.py cùng cấp
from ..forms import AddWorkspaceMemberForm, EditWorkspaceMemberForm
from core.views import ErrorView # Giả định bạn có ErrorView trong core.views
from django.utils import timezone # Để sử dụng timezone.now() cho soft delete

User = get_user_model() # Lấy User model hiện tại

class WorkspaceMembersListView(LoginRequiredMixin, View):
    template_name = 'Member_List.html' # Đảm bảo tên template đúng như bạn đã chỉ ra

    def get(self, request, pk):
        workspace = get_object_or_404(Workspace, pk=pk, deleted_at__isnull=True)
        print(f"DEBUG: Trong WorkspaceMembersListView.get, workspace.pk là: {workspace.pk}")
        # Lấy các thành viên của workspace, loại trừ những người đã bị soft-deleted
        members = WorkspaceMember.objects.filter(
            workspace=workspace,
            deleted_at__isnull=True
        ).order_by('joined_at')

        # Kiểm tra quyền: Chỉ admin của workspace mới được quản lý thành viên
        # Một người dùng là admin nếu có một WorkspaceMember liên kết với họ và isAdmin=True
        is_admin = WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user,
            isAdmin=True,
            deleted_at__isnull=True # Đảm bảo bản ghi thành viên của admin cũng không bị xóa mềm
        ).exists()

        # Form để thêm thành viên mới
        # Truyền instance của workspace để form có thể kiểm tra người dùng đã tồn tại
        add_member_form = AddWorkspaceMemberForm(workspace=workspace)

        context = {
            'workspace': workspace,
            'members': members,
            'is_admin': is_admin,
            'add_member_form': add_member_form,
            'current_user_id': request.user.id,
            'workspace_pk': workspace.pk, # THÊM DÒNG NÀY ĐỂ TRUYỀN PK RIÊNG BIỆT
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        workspace = get_object_or_404(Workspace, pk=pk, deleted_at__isnull=True)

        # Kiểm tra quyền: Chỉ admin của workspace mới được thêm thành viên
        is_admin = WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user,
            isAdmin=True,
            deleted_at__isnull=True
        ).exists()

        if not is_admin:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền thêm thành viên vào workspace này.'}, status=403)

        # Form sẽ nhận request.POST và workspace để xử lý
        add_member_form = AddWorkspaceMemberForm(request.POST, workspace=workspace)

        if add_member_form.is_valid():
            # user_to_add đã được gán vào cleaned_data['user'] trong form's clean_username method
            user_to_add = add_member_form.cleaned_data['user'] 
            permission = add_member_form.cleaned_data['permission']
            is_admin_member = add_member_form.cleaned_data['isAdmin']

            try:
                # Tạo WorkspaceMember mới
                WorkspaceMember.objects.create(
                    workspace=workspace,
                    user=user_to_add,
                    permission=permission,
                    isAdmin=is_admin_member
                )
                return JsonResponse({'success': True, 'message': f'Thành viên {user_to_add.username} đã được thêm thành công.'})
            except IntegrityError:
                # Trường hợp này có thể xảy ra nếu có một thành viên đã soft-deleted nhưng vẫn có unique_together
                # Mặc dù form đã kiểm tra deleted_at__isnull=True, vẫn nên có phòng ngừa
                return JsonResponse({'success': False, 'error': 'Người dùng này đã là thành viên của workspace.'}, status=400)
            except Exception as e:
                # Xử lý các lỗi khác
                print(f"Error adding workspace member: {e}") # Để debug
                return JsonResponse({'success': False, 'error': f'Lỗi không xác định khi thêm thành viên: {e}'}, status=500)
        else:
            # Nếu form không hợp lệ, trả về lỗi validation để hiển thị trên frontend
            return JsonResponse({'success': False, 'errors': add_member_form.errors.as_json()}, status=400)


# View để chỉnh sửa quyền của thành viên (Xử lý AJAX POST)
class EditWorkspaceMemberView(LoginRequiredMixin, View):
    def post(self, request, pk, member_id):
        # Lấy workspace và thành viên cần chỉnh sửa, đảm bảo cả hai chưa bị xóa mềm
        workspace = get_object_or_404(Workspace, pk=pk, deleted_at__isnull=True)
        member_to_edit = get_object_or_404(WorkspaceMember, pk=member_id, workspace=workspace, deleted_at__isnull=True)

        # Kiểm tra quyền: Chỉ admin của workspace mới được chỉnh sửa thành viên khác
        is_admin = WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user,
            isAdmin=True,
            deleted_at__isnull=True
        ).exists()

        if not is_admin:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền chỉnh sửa thành viên trong workspace này.'}, status=403)

        # Ngăn chặn người dùng tự chỉnh sửa quyền isAdmin của chính mình qua API này
        # (Để tránh trường hợp người dùng tự hạ quyền admin của mình và không thể khôi phục)
        if member_to_edit.user == request.user and 'isAdmin' in request.POST:
            # Nếu người dùng cố gắng bỏ quyền admin của chính họ
            if member_to_edit.isAdmin and request.POST.get('isAdmin') != 'true':
                return JsonResponse({'success': False, 'error': 'Bạn không thể tự bỏ quyền quản trị của mình.'}, status=400)
            # Hoặc cố gắng thay đổi quyền khác của chính họ
            if member_to_edit.get_permission_display() != request.POST.get('permission'):
                 return JsonResponse({'success': False, 'error': 'Bạn không thể tự thay đổi quyền hạn của mình qua API này. Vui lòng liên hệ admin khác.'}, status=400)

        form = EditWorkspaceMemberForm(request.POST, instance=member_to_edit)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': f'Quyền của thành viên {member_to_edit.user.username} đã được cập nhật.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)


# View để xóa thành viên (Xử lý AJAX POST)
class DeleteWorkspaceMemberView(LoginRequiredMixin, View):
    def post(self, request, pk, member_id):
        # Lấy workspace và thành viên cần xóa, đảm bảo cả hai chưa bị xóa mềm
        workspace = get_object_or_404(Workspace, pk=pk, deleted_at__isnull=True)
        member_to_delete = get_object_or_404(WorkspaceMember, pk=member_id, workspace=workspace, deleted_at__isnull=True)

        # Kiểm tra quyền: Chỉ admin của workspace mới được xóa thành viên
        is_admin = WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user,
            isAdmin=True,
            deleted_at__isnull=True
        ).exists()

        if not is_admin:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền xóa thành viên khỏi workspace này.'}, status=403)

        # Ngăn chặn người dùng tự xóa mình ra khỏi workspace
        if member_to_delete.user == request.user:
            return JsonResponse({'success': False, 'error': 'Bạn không thể tự xóa mình ra khỏi workspace.'}, status=400)

        try:
            # Soft delete thành viên
            member_to_delete.deleted_at = timezone.now()
            member_to_delete.save()
            return JsonResponse({'success': True, 'message': f'Thành viên {member_to_delete.user.username} đã được xóa khỏi workspace.'})
        except Exception as e:
            print(f"Error deleting workspace member: {e}") # Để debug
            return JsonResponse({'success': False, 'error': f'Lỗi không xác định khi xóa thành viên: {e}'}, status=500)