from django.http import Http404, JsonResponse
from core.views.BaseView import BaseView # Đảm bảo BaseView được import đúng
from django.core.paginator import Paginator
from notes.models import Note
from comments.models import Comment


class CommentListView(BaseView):
    def get(self, request, note_id):
        page = request.GET.get("page", 1)
        page_size = 5

        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            raise Http404("Note không tồn tại.")

        # Lấy các comment gốc (parent_comment = null)
        # Đã sửa lỗi FieldError bằng cách đổi 'parentComment' thành 'parent_comment'
        comments = Comment.objects.filter(
            note=note,
            parent_comment__isnull=True, # ĐÃ SỬA TÊN TRƯỜNG TẠI ĐÂY
            deleted_at__isnull=True
        ).select_related("user").order_by("-created_at")

        paginator = Paginator(comments, page_size)
        page_obj = paginator.get_page(page)

        comment_list = []
        for comment in page_obj:
            comment_list.append({
                "id": comment.id,
                "user": comment.user.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                # Nếu bạn muốn hiển thị cả comment con (replies), bạn sẽ cần thêm logic ở đây
                # Ví dụ: "replies": self.get_replies(comment)
            })

        return JsonResponse({
            "comments": comment_list,
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
            "total_comments": paginator.count,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        })