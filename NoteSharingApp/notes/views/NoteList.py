
from django.http import JsonResponse

from core.views.BaseView import BaseView
from notes.models import Note
from notes.models import NoteShare
from django.db.models import Q
from django.core.paginator import Paginator

class NoteListView(BaseView):
  
  #Lấy danh sach note 
  #/notes/?permission=edit
  #/notes/?created_by_me=true&search=plan&page=2
  def get(self, request):
    user = request.user
    page = request.GET.get("page", 1)
    page_size = 10

    # ----- Filter -----
    search = request.GET.get("search")
    permission_filter = request.GET.get("permission")       # view/edit
    created_by_me = request.GET.get("created_by_me") == "true"

    # ----- Cơ bản: Lấy note của user hoặc được share -----
    if created_by_me:
        notes = Note.objects.filter(create_by=user)
    else:
        notes = Note.objects.filter(
            Q(create_by=user) |
            Q(id__in=NoteShare.objects.filter(share_with=user).values_list("note_id", flat=True))
        )

    notes = notes.filter(deleted_at__isnull=True)

    # ----- Áp dụng filter -----
    if search:
        notes = notes.filter(title__icontains=search)

    notes = notes.select_related("create_by").order_by("-updated_at")

    # ----- Phân trang -----
    paginator = Paginator(notes, page_size)
    page_obj = paginator.get_page(page)

    note_list = []
    for note in page_obj.object_list:
        if note.create_by == user:
            permission = "owner"
        else:
            share = NoteShare.objects.filter(note=note, share_with=user).first()
            permission = share.permission 

        note_list.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "create_by": note.create_by.username,
            "permission": permission,
            "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M")
        })

    return JsonResponse({
        "notes": note_list,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_notes": paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })