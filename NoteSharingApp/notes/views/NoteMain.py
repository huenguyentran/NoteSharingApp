from django.shortcuts import render
from core.views.BaseView import BaseView

#Trang danh sach note + chinh sua note + chinh sua share note
# chon 1 note -> den trang rieng cho note do
class NoteMainView(BaseView):
  def get(self, request):
    return render(request, 'Note/NoteMain.html')
  