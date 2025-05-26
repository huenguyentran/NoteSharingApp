from django.db import models
from django.contrib.auth.models import User
from workspaces.models import Workspace as workspace

class Note(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField()              
    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes'
    )  

    workspace = models.ForeignKey(
        workspace,
        on_delete=models.CASCADE,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return self.title
    
class NoteShare(models.Model):
    note = models.ForeignKey(
        Note, 
        on_delete=models.CASCADE
    )
    share_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='share_sender'
    )
    share_with = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='share_receiver'
    )
    permission = models.CharField(
        max_length=50, 
        choices=[('view', 'View'), ('edit', 'Edit')], 
        default='view'
    )

    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.title} shared with {self.share_with.username}"
    
class Comment(models.Model):
    note = models.ForeignKey(
        Note, 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Comment by {self.user.username} on {self.note.title}"