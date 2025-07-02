from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
# Đảm bảo bạn import tất cả các view cần thiết
from .views import (
    WorkspaceListView, WorkspaceMainView, MemberListView, DetailWorkspaceView,
    GetNotesWorkspaceView, FileWorkspaceListView, CreateWorkspaceView,
    DeleteWorkspaceView, WorkspaceFileView, WorkspaceMemberView, UpdateWorkspaceView
)
from .views.workspaceMembers import (
    WorkspaceMembersListView, EditWorkspaceMemberView, DeleteWorkspaceMemberView
)


urlpatterns = [
    # MainView dùng trong navigation
    path("MainView/", WorkspaceMainView.as_view(), name="workspace_main"),

    # Danh sách workspace của người dùng (API endpoint cho JS và hiển thị HTML ban đầu)
    path("", WorkspaceListView.as_view(), name="workspace_list"),

    # Màn hình xem chi tiết 1 workspace
    path('<int:pk>/', DetailWorkspaceView.as_view(), name='workspace_detail'),

    # Tạo mới một workspace
    path('create/', CreateWorkspaceView.as_view(), name="create_workspace"),

    # Xóa một workspace cụ thể (thêm <int:pk>)
    path('<int:pk>/delete/', DeleteWorkspaceView.as_view(), name="delete_workspace"),

    # Cập nhật một workspace cụ thể
    path('<int:pk>/update/', UpdateWorkspaceView.as_view(), name='update_workspace'),

    # Danh sách Notes của Workspace
    path("<int:pk>/notes/", GetNotesWorkspaceView.as_view(), name="workspace_notes_list"),

    # Danh sách Files của Workspace
    path("<int:pk>/files/", FileWorkspaceListView.as_view(), name="workspace_files_list"), # Đã thêm / ở cuối để nhất quán

    # Xóa, thêm 1 file (API cho file trong workspace)
    # Giả định WorkspaceFileView xử lý POST/DELETE cho file, cần pk của file đó
    # Nếu nó liên quan đến workspace, URL cần có pk của workspace nữa
    path('files/<int:file_pk>/', WorkspaceFileView.as_view(), name="file_workspace"), # Đổi pk thành file_pk để rõ ràng hơn

    # Quản lý thành viên của một Workspace cụ thể
    # Đây là danh sách các thành viên trong một workspace
    path('<int:pk>/members/', WorkspaceMembersListView.as_view(), name='workspace_members_list'),
    
    # Thêm thành viên vào một workspace cụ thể
    # Giả định WorkspaceMemberView xử lý việc thêm/cập nhật thành viên
    path('<int:pk>/members/add/', WorkspaceMemberView.as_view(), name='add_workspace_member'), # URL mới cho thêm thành viên

    # Chỉnh sửa quyền của thành viên trong workspace (ví dụ: admin/unadmin)
    path('<int:pk>/members/edit/<int:member_id>/', EditWorkspaceMemberView.as_view(), name='edit_workspace_member'),
    
    # Xóa thành viên khỏi workspace
    path('<int:pk>/members/delete/<int:member_id>/', DeleteWorkspaceMemberView.as_view(), name='delete_workspace_member'),

    # Nếu MemberListView có mục đích khác (ví dụ: danh sách thành viên chung, không thuộc workspace cụ thể)
    # thì URL của nó cần khác hoàn toàn hoặc nó nên được loại bỏ nếu đã được WorkspaceMembersListView bao phủ.
    # Hiện tại tôi đã comment nó để tránh trùng lặp.
    # path("<int:pk>/members/", MemberListView.as_view(), name="workspace_members_list_legacy"),
]