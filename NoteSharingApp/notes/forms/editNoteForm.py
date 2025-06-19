from django import forms

from notes.models import Note

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'id': 'note-content'})
        }