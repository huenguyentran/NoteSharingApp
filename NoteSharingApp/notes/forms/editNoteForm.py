from django import forms
from notes.models import Note

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'content',
            'is_shared_via_link',
            'link_permission'
        ]
        labels = {
            'title': 'Tiêu đề',
            'content': 'Nội dung',
            'is_shared_via_link': 'Chia sẻ bằng link',
            'link_permission': 'Quyền chia sẻ qua link'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập nội dung ghi chú',
                'rows': 8,
                'id': 'note-content'
            }),
            'is_shared_via_link': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'link_permission': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
