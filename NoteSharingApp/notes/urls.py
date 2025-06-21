from django.urls import path

from .views import createNoteView, editNoteView, viewNoteView, shareNoteView, deleteNoteView

urlpatterns = [
    #note URLs

    path('create/', createNoteView.as_view(), name='create_note'),

    path("<int:note_id>/", viewNoteView.as_view(), name="view_note"),

    path("edit/<int:note_id>/", editNoteView.as_view(), name="edit_note"),

    path("delete/<int:note_id>/", deleteNoteView.as_view(), name="delete_note"),

    path("sharing/<int:note_id>/", shareNoteView.as_view(), name="share_note"),
]