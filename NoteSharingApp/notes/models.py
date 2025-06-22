from datetime import timezone
import uuid
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

    is_shared_via_link = models.BooleanField(default=False)
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    link_permission = models.CharField(
        max_length=10,
        choices=[('view', 'View'), ('edit', 'Edit')],
        default='view'
    )

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return self.title
    

    def get_permission(self, user=None, token=None):
        if user and self.create_by == user:
            return 'owner'

        if user:
            share = self.shares.filter(share_with=user).first()
            if share:
                return share.permission

        if token and self.is_shared_via_link and str(self.share_token) == str(token):
            return self.link_permission

        return None
    
    def enable_share_link(self, permission='view'):
        self.is_shared_via_link = True
        self.link_permission = permission
        self.save()
        return self.get_share_link()

    def get_share_link(self):
        return f'/note/by-link/{self.id}/?token={self.share_token}'
    

    
class NoteShare(models.Model):
    note = models.ForeignKey(
        Note, 
        on_delete=models.CASCADE,
        related_name='shares'
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
