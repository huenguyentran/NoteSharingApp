from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note, NoteShare
from django.core.paginator import Paginator # <-- THÊM DÒNG NÀY

from .BaseView import BaseView

class DashBoardView(BaseView, View):
    def get(self, request):
        # --- Phân trang cho "My Notes" ---
        my_notes_list = Note.objects.filter(
            create_by=request.user, 
            deleted_at__isnull=True
        ).order_by('-created_at') # Sắp xếp để phân trang nhất quán (mới nhất trước)

        # Tạo đối tượng Paginator cho My Notes (6 notes mỗi trang)
        my_notes_paginator = Paginator(my_notes_list, 6) 
        
        # Lấy số trang hiện tại cho My Notes từ tham số URL 'my_page'
        my_page_number = request.GET.get('my_page') 
        
        # Lấy đối tượng Page cho My Notes
        # .get_page() xử lý trường hợp tham số không hợp lệ (ví dụ: chuỗi, số âm)
        my_notes_page_obj = my_notes_paginator.get_page(my_page_number)


        # --- Phân trang cho "Notes Shared With Me" ---
        shared_notes_list = NoteShare.objects.filter(
            share_with=request.user,
            note__deleted_at__isnull=True
        ).select_related('note', 'share_by').order_by('-shared_at') # Sắp xếp (mới nhất trước)

        # Tạo đối tượng Paginator cho Shared Notes (6 notes mỗi trang)
        shared_notes_paginator = Paginator(shared_notes_list, 6)

        # Lấy số trang hiện tại cho Shared Notes từ tham số URL 'shared_page'
        shared_page_number = request.GET.get('shared_page')

        # Lấy đối tượng Page cho Shared Notes
        shared_notes_page_obj = shared_notes_paginator.get_page(shared_page_number)


        return render(request, 'dashboard/dashboard.html', {
            'notes': my_notes_page_obj,        # <-- TRUYỀN ĐỐI TƯỢNG PAGE NÀY
            'shared_notes': shared_notes_page_obj # <-- TRUYỀN ĐỐI TƯỢNG PAGE NÀY
        })