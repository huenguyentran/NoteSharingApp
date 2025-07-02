from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse # <--- THÊM DÒNG NÀY

from workspaces.models import Workspace
# from django.core.serializers import serialize # Không cần dùng serialize trực tiếp nữa nếu bạn build dict

class WorkspaceListView(LoginRequiredMixin, ListView):
    model = Workspace
    template_name = 'Workspace_List.html'
    context_object_name = 'workspaces'
    paginate_by = 10 

    def get_queryset(self):
        # Lấy queryset của các workspace mà người dùng hiện tại là chủ sở hữu hoặc thành viên
        from django.db.models import Q # Import Q
        queryset = Workspace.objects.filter(
            Q(owner=self.request.user) | Q(members__user=self.request.user, members__deleted_at__isnull=True)
        ).distinct() # Dùng distinct() để tránh trùng lặp nếu một workspace có nhiều thành viên là cùng user

        # Thêm điều kiện để chỉ lấy những workspace chưa bị xóa mềm
        queryset = queryset.filter(deleted_at__isnull=True)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset.order_by('-created_at')

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest' or self.request.GET.get('format') == 'json':
            workspaces = context['workspaces']
            workspace_data = []
            for workspace in workspaces:
                workspace_data.append({
                    'id': workspace.id,
                    'pk': workspace.pk, # Thêm pk để dễ dàng truy cập trong JS
                    'name': workspace.name,
                    'description': workspace.description,
                    'owner_username': workspace.owner.username,
                    'created_at': workspace.created_at.isoformat(),
                    'updated_at': workspace.updated_at.isoformat(),
                    # SỬA CÁC URL DƯỚI ĐÂY BẰNG CÁCH SỬ DỤNG reverse()
                    'view_url': reverse('workspace_detail', args=[workspace.pk]),
                    'edit_url': reverse('update_workspace', args=[workspace.pk]),
                    'delete_url': reverse('delete_workspace', args=[workspace.pk]),
                })

            paginator = context.get('paginator')
            page_obj = context.get('page_obj')
            
            response_data = {
                'workspaces': workspace_data,
                'page_info': {
                    'current_page': page_obj.number if page_obj else 1,
                    'total_pages': paginator.num_pages if paginator else 1,
                    'has_next': page_obj.has_next() if page_obj else False,
                    'has_previous': page_obj.has_previous() if page_obj else False,
                    'search_query': self.request.GET.get('q', '') # Thêm search_query để hiển thị thông báo
                }
            }
            return JsonResponse(response_data)
        else:
            return super().render_to_response(context, **response_kwargs)