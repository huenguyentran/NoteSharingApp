from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import WorkspaceListView, WorkspaceMainView, MemberListView, DetailWorkspaceView
from .views import NoteWorkspaceListView, FileWorkspaceListView, CreateWorkspaceView, DeleteWorkspaceView, WorkspaceFileView
from .views import WorkspaceMemberView, UpdateWorkspaceView


urlpatterns = [
    #MainView dùng trong navigation
    path("MainView/", WorkspaceMainView.as_view(), name="workspace_main"),

    #Danh sách workspace của người dùng
    path("", WorkspaceListView.as_view(), name="workspace_list"),

    #Danh sách thành viên của Workspace
    path("<int:pk>/members/", MemberListView.as_view(), name="workspace_members_list"),

    #Danh sách Notes của Workspace
    path("<int:pk>/notes/", NoteWorkspaceListView.as_view(), name="workspace_notes_list"),

    #Danh sách Files của note
    path("<int:pk>/files", FileWorkspaceListView.as_view(), name="workspace_files_list"),

    #Màng hình xem 1 workspace
    path('<int:pk>/', DetailWorkspaceView.as_view(), name='workspace_detail'),

    path('create/', CreateWorkspaceView.as_view(), name="create_workspace"),

    path('delete/', DeleteWorkspaceView.as_view(), name="delete_workspace"),

    path('<int:pk>/update/', UpdateWorkspaceView.as_view(), name='update_workspace'),

    #Xóa, thêm 1 file -> json truyền file Id
    path('files/<int:pk>', WorkspaceFileView.as_view(), name="file_workspace"),

    #Chỉnh sửa admin/unadmin + thêm người vào nhóm
    path('members/', WorkspaceMemberView.as_view(), name='workspace_member'),

]