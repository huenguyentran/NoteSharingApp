from django.shortcuts import render, redirect
from django.views import View
from notes.models import Note, NoteShare
from django.core.paginator import Paginator
from django.db.models import Q # <-- THÊM DÒNG NÀY ĐỂ SỬ DỤNG Q OBJECTS CHO TÌM KIẾM PHỨC TẠP

from .BaseView import BaseView

class DashBoardView(BaseView, View):
    def get(self, request):
        # Lấy chuỗi tìm kiếm từ tham số GET 'q'
        search_query = request.GET.get('q', '') 

        # --- Phân trang và tìm kiếm cho "My Notes" ---
        my_notes_queryset = Note.objects.filter(
            create_by=request.user, 
            deleted_at__isnull=True
        ).order_by('-created_at')

        # Áp dụng bộ lọc tìm kiếm nếu có query
        if search_query:
            my_notes_queryset = my_notes_queryset.filter(
                Q(title__icontains=search_query) | # Tìm kiếm trong tiêu đề (không phân biệt chữ hoa/thường)
                Q(content__icontains=search_query) # Hoặc trong nội dung
            )

        my_notes_paginator = Paginator(my_notes_queryset, 6) 
        my_page_number = request.GET.get('my_page') 
        my_notes_page_obj = my_notes_paginator.get_page(my_page_number)


        # --- Phân trang và tìm kiếm cho "Notes Shared With Me" ---
        shared_notes_queryset = NoteShare.objects.filter(
            share_with=request.user,
            note__deleted_at__isnull=True
        ).select_related('note', 'share_by').order_by('-shared_at')

        # Áp dụng bộ lọc tìm kiếm cho shared notes nếu có query
        if search_query:
            shared_notes_queryset = shared_notes_queryset.filter(
                Q(note__title__icontains=search_query) | # Tìm kiếm trong tiêu đề của note được chia sẻ
                Q(note__content__icontains=search_query) # Hoặc trong nội dung của note được chia sẻ
            )

        shared_notes_paginator = Paginator(shared_notes_queryset, 6)
        shared_page_number = request.GET.get('shared_page')
        shared_notes_page_obj = shared_notes_paginator.get_page(shared_page_number)

        return render(request, 'dashboard/dashboard.html', {
            'notes': my_notes_page_obj,
            'shared_notes': shared_notes_page_obj,
            'search_query': search_query, # <-- TRUYỀN CHUỖI TÌM KIẾM ĐỂ GIỮ NÓ TRONG Ô INPUT
        })