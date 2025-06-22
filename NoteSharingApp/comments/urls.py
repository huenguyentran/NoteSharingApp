from django.urls import path

from .views import CommentListView, CommentView

#URL: /comments
urlpatterns = [
  #/comments/note/1/?page=1
  path('note/<uuid:note_id>/', CommentListView.as_view(), name='comment_list'),
  path('comments/<int:comment_id>/', CommentView.as_view(), name='edit_or_delete')
    
]