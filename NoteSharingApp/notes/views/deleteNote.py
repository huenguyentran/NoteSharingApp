from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from core.views import ErrorView
from notes.models import Note
from core.views.BaseView import BaseView

from django.utils import timezone

class deleteNoteView(BaseView): 
    def post(self, request, note_id):
        try:
            note = request.user.notes.get(id=note_id, deleted_at__isnull=True)
        except Note.DoesNotExist:
            return ErrorView(request, "Không tìm thấy ghi chú!", status=404)

        if note.create_by != request.user:
            return JsonResponse({'permission_error': 'Bạn không có quyền xóa ghi chú này.'})

        note.deleted_at = timezone.now()
        note.save()
        return JsonResponse({'success': True})
