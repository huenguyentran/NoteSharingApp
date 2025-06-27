from django.urls import path

from .views import createNoteView, editNoteView, viewNoteView, shareNoteView, deleteNoteView, ByLinkNoteView, NoteMainView, NoteListView

#URL: /notes
urlpatterns = [
    #note URLs
    
    #URL: /
    #Query: search, page
    path('', NoteListView.as_view(), name='note_list'),

    path('noteMainView/', NoteMainView.as_view(), name='note_main'),

    path('create/', createNoteView.as_view(), name='create_note'),

    #Bam vào note ở trang main note -> gọi note (trang này có nội dung note + comment thuộc note đó)
    path("<int:note_id>/", viewNoteView.as_view(), name="view_note"),

    path("edit/<int:note_id>/", editNoteView.as_view(), name="edit_note"),

    path("delete/<int:note_id>/", deleteNoteView.as_view(), name="delete_note"),

    path("sharing/<int:note_id>/", shareNoteView.as_view(), name="share_note"),

    path('by-link/<int:note_id>/', ByLinkNoteView.as_view(), name='note_by_link')

]