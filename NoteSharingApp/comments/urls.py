# comments/urls.py
from django.urls import path
# Đảm bảo import đúng đường dẫn tới các view của bạn
# Dựa trên cấu trúc thư mục:
# comments/views/comment.py
# comments/views/CommentList.py
from .views.comment import CommentView # Import CommentView từ comment.py
from .views.CommentList import CommentListView # Import CommentListView từ CommentList.py


urlpatterns = [
    # API để tạo comment mới (POST request sẽ đến endpoint này)
    # Ví dụ: /api/comments/create/
    path('create/', CommentView.as_view(), name='comment_create'),

    # API để lấy danh sách comment cho một note (GET request)
    # Ví dụ: /api/comments/note/123/?page=1
    path('note/<int:note_id>/', CommentListView.as_view(), name='comments_list_by_note'),

    # API để sửa (PUT) hoặc xóa (DELETE) một comment cụ thể
    # Ví dụ: /api/comments/456/ (trong đó 456 là comment_id)
    path('<int:comment_id>/', CommentView.as_view(), name='comment_detail'),
]