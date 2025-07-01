from django import forms
from notes.models import Note

class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'content',
            'is_shared_via_link', # Thêm trường này
            'link_permission'     # Thêm trường này
        ]
        labels = {
            'title': 'Tiêu đề',
            'content': 'Nội dung',
            'is_shared_via_link': 'Chia sẻ bằng link', # Nhãn cho checkbox
            'link_permission': 'Quyền chia sẻ qua link' # Nhãn cho select
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