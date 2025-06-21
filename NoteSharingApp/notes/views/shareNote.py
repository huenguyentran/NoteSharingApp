from django.views import View
from core.views.ErrorView import ErrorView
from notes.models import NoteShare, Note
from core.views.BaseView import BaseView


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class shareNoteView(BaseView):
    template_name = 'share_note.html'
    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)

        if note.create_by != request.user:
            return render(request, self.template_name, {
                'error': 'Bạn không có quyền chia sẻ ghi chú này.',
                'note': note
            })
        users = User.objects.exclude(id=request.user.id)
        shared_users = NoteShare.objects.filter(note=note)

        # Trong cả GET và POST:
        return render(request, self.template_name, {
            'note': note,
            'users': User.objects.exclude(id=request.user.id),
            'shared_users': shared_users,
        })
    

    def post(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        if note.create_by != request.user:
            return ErrorView(request, "Bạn không có quyền chia sẻ ghi chú này", status=404)
        
        if 'share_with_ids' in request.POST:
            share_with_ids = request.POST.getlist('share_with_ids')
            permission = request.POST.get('permission')

            users_shared = []
            for uid in share_with_ids:
                try:
                    user = User.objects.get(id=uid)
                    NoteShare.objects.update_or_create(
                        note=note,
                        share_with=user,
                        defaults={'share_by': request.user, 'permission': permission}
                    )
                    users_shared.append(user.username)
                except User.DoesNotExist:
                    continue 
            shared_users = NoteShare.objects.filter(note=note)

            return render(request, self.template_name, {
                'note': note,
                'users': User.objects.exclude(id=request.user.id),
                'shared_users': shared_users,
            })
        

    
        elif 'update_permissions' in request.POST:
            for share in NoteShare.objects.filter(note=note):
                new_perm = request.POST.get(f'update_permission_{share.id}')
                if new_perm in ['view', 'edit'] and share.permission != new_perm:
                    share.permission = new_perm
                    share.save()
                return render(request, 'share_note.html', {
                    'note': note,
                    'users': User.objects.exclude(id=request.user.id),
                    'shared_users': NoteShare.objects.filter(note=note),
                    'success': "Cập nhật quyền thành công!",
                })
            



        elif 'delete_share_id' in request.POST: 
            share_id = request.POST.get('delete_share_id')
            note = get_object_or_404(Note, id=note_id)
            share = NoteShare.objects.filter(id=share_id, note=note).first()
            if share:
                share.delete()
                return render(request, 'share_note.html', {
                    'note': note,
                    'users': User.objects.exclude(id=request.user.id),
                    'shared_users': NoteShare.objects.filter(note=note),
                    'success': "Hủy chia sẻ thành công!",
                })
            else:
                return render(request, 'share_note.html', {
                    'note': note,
                    'users': User.objects.exclude(id=request.user.id),
                    'shared_users': NoteShare.objects.filter(note=note),
    '               error': 'Hủy chia sẻ không thành công.',
                })
 
