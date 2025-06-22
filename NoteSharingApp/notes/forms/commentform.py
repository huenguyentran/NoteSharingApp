from django import forms
from notes.models import Comment 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['note', 'parentComment', 'content']

        widgets = {
            'note': forms.HiddenInput(),
            'parentComment': forms.HiddenInput(),
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Viết bình luận...',
                'class': 'form-control'
            }),
        }