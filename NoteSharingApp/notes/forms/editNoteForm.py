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
            'title': 'Title',
            'content': 'Content',
            'is_shared_via_link': 'Share via Link',
            'link_permission': 'Link Permission'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note content',
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