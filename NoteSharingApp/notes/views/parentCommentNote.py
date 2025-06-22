from datetime import timezone
from django.shortcuts import get_object_or_404
from NoteSharingApp.core.views import BaseView
from django.http import JsonResponse
from NoteSharingApp.notes.models import Comment
from NoteSharingApp.notes.models import Note
import json


class parentCommentView(BaseView):
  def get(request, note_id):

    comments = Comment.objects.filter(note_id=note_id, deleted_at__isnull=True, parentComment__isnull = True).order_by('created_at')

    data = []
    for c in comments:
        data.append({
            'id': c.id,
            'user': c.user.username,
            'content': c.content,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M'),
            'parent_id': c.parentComment.id if c.parentComment else None
        })

    return JsonResponse({'comments': data})
  

  #CreateComment
  def post(request):
    data = json.loads(request.body)
    content = data.get("content", "").strip()
    note_id = data.get("note")
    parent_id = data.get("parentComment", None)

    if not content or not note_id:
        return JsonResponse({"error": "Thiếu nội dung hoặc note_id"}, status=400)

    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "Note không tồn tại"}, status=404)

    parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

    comment = Comment.objects.create(
        note=note,
        parentComment=parent,
        user=request.user, 
        content=content
    )

    return JsonResponse({
        "success": True,
        "comment": {
            "id": comment.id,
            "user": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M'),
            "parent_id": comment.parentComment.id if comment.parentComment else None
        }
    })
  

  def put(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({'error': 'Không có quyền sửa bình luận này.'}, status=403)

    data = json.loads(request.body)
    content = data.get("content", "").strip()

    if not content:
        return JsonResponse({'error': 'Nội dung không được để trống.'}, status=400)

    comment.content = content
    comment.updated_at = timezone.now()
    comment.save()

    return JsonResponse({'success': True, 'message': 'Đã cập nhật bình luận.'})