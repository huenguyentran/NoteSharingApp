from django import forms
from notes.models import Note

class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'content',
            'is_shared_via_link', # Add this field
            'link_permission'     # Add this field
        ]
        labels = {
            'title': 'Title',
            'content': 'Content',
            'is_shared_via_link': 'Share via Link', # Label for checkbox
            'link_permission': 'Link Permission' # Label for select
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