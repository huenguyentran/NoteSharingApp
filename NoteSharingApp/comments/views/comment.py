# comments/views.py
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.utils import timezone
import json
from comments.models import Comment
from notes.models import Note

class CommentView(View):
    def post(self, request):
        """
        Yêu cầu JSON: { "note_id": <id>, "content": <text> }
        """
        try:
            data = json.loads(request.body)
            note_id = data.get("note_id")
            content = data.get("content", "").strip()
        except:
            return JsonResponse({"error": "Dữ liệu không hợp lệ"}, status=400)

        if not content or not note_id:
            return JsonResponse({"error": "Thiếu nội dung hoặc note_id"}, status=400)

        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            raise Http404("Note không tồn tại.")

        comment = Comment.objects.create(
            note=note,
            user=request.user,
            content=content
        )

        return JsonResponse({
            "message": "Tạo comment thành công",
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
        })

    def put(self, request, comment_id):
        """
        Yêu cầu JSON: { "content": <text> }
        """
        try:
            comment = Comment.objects.get(id=comment_id, deleted_at__isnull=True)
        except Comment.DoesNotExist:
            raise Http404("Comment không tồn tại.")

        if request.user != comment.user:
            return HttpResponseForbidden("Bạn không có quyền sửa comment này.")

        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()
        except:
            return JsonResponse({"error": "Dữ liệu không hợp lệ"}, status=400)

        if not content:
            return JsonResponse({"error": "Nội dung không được để trống"}, status=400)

        comment.content = content
        comment.updated_at = timezone.now()
        comment.save()

        return JsonResponse({
            "message": "Cập nhật thành công",
            "content": comment.content
        })

    def delete(self, request, comment_id):
        """
        Xoá mềm comment (đánh dấu deleted_at).
        """
        try:
            comment = Comment.objects.get(id=comment_id, deleted_at__isnull=True)
        except Comment.DoesNotExist:
            raise Http404("Comment không tồn tại.")

        if request.user != comment.user:
            return HttpResponseForbidden("Bạn không có quyền xoá comment này.")

        comment.deleted_at = timezone.now()
        comment.save()

        return JsonResponse({"message": "Đã xoá comment"})
