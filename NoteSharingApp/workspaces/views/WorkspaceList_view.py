from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse # Import JsonResponse

from workspaces.models import Workspace # Đảm bảo Workspace và các mô hình liên quan được import
from django.core.serializers import serialize # Để serialize queryset thành JSON
import json # Để parse lại JSON nếu cần, nhưng serialize đã đủ

class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    template_name = 'Workspace_List.html'
    context_object_name = 'workspaces'
    paginate_by = 10 # Thêm phân trang nếu bạn muốn, ví dụ 10 workspaces mỗi trang

    def get_queryset(self):
        # Lấy queryset của các workspace mà người dùng hiện tại là thành viên
        queryset = Workspace.objects.filter(members__user=self.request.user).distinct()

        # Xử lý tìm kiếm nếu có tham số 'q'
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) # Tìm kiếm theo tên workspace

        return queryset.order_by('-created_at') # Sắp xếp theo ngày tạo mới nhất

    def render_to_response(self, context, **response_kwargs):
        # Kiểm tra nếu yêu cầu là AJAX (từ JavaScript của bạn)
        # Hoặc nếu bạn muốn API endpoint luôn trả về JSON khi truy cập URL cụ thể
        # Bạn có thể thêm một tham số query string, ví dụ: ?format=json
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest' or self.request.GET.get('format') == 'json':
            workspaces = context['workspaces']
            # Chuyển đổi queryset thành list các dictionary để dễ dàng serialize
            # Hoặc bạn có thể dùng serialize trực tiếp nếu cấu trúc JSON phù hợp
            workspace_data = []
            for workspace in workspaces:
                workspace_data.append({
                    'id': workspace.id,
                    'name': workspace.name,
                    'description': workspace.description, # Giả sử có trường description
                    'owner_username': workspace.owner.username,
                    'created_at': workspace.created_at.isoformat(), # Chuyển đổi datetime sang định dạng ISO 8601
                    'updated_at': workspace.updated_at.isoformat(), # Chuyển đổi datetime sang định dạng ISO 8601
                    'view_url': workspace.get_absolute_url(), # Nếu bạn có get_absolute_url trong model Workspace
                    'edit_url': f'/workspaces/edit/{workspace.id}/', # Thay bằng URL thực tế của bạn
                    'delete_url': f'/workspaces/delete/{workspace.id}/', # Thay bằng URL thực tế của bạn
                })

            # Xử lý dữ liệu phân trang
            # Nếu bạn có phân trang, cần trả về thông tin phân trang
            paginator = context.get('paginator')
            page_obj = context.get('page_obj')
            
            response_data = {
                'workspaces': workspace_data,
                'page_info': {
                    'current_page': page_obj.number if page_obj else 1,
                    'total_pages': paginator.num_pages if paginator else 1,
                    'has_next': page_obj.has_next() if page_obj else False,
                    'has_previous': page_obj.has_previous() if page_obj else False,
                    # Có thể thêm next_page_url, previous_page_url nếu cần
                }
            }
            return JsonResponse(response_data)
        else:
            # Nếu không phải là yêu cầu AJAX, render template như bình thường
            # Điều này chủ yếu để đảm bảo template của bạn vẫn có thể hiển thị thông báo "Loading..."
            # và các thành phần khác trước khi JS tải dữ liệu.
            return super().render_to_response(context, **response_kwargs)