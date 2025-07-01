# notes/models.py
# Removed: from datetime import timezone (if not used elsewhere in this file)
import uuid
from django.db import models
from django.contrib.auth.models import User
from workspaces.models import Workspace as WorkspaceModel # Đổi tên import để tránh trùng với tên trường 'workspace'

from dotenv import load_dotenv
load_dotenv()

import os
HOST_URL = os.getenv("LOCALHOST_URL")

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    workspace = models.ForeignKey(
        WorkspaceModel, # Sử dụng tên đã đổi
        on_delete=models.CASCADE,
        null=True,
        blank=True
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
            # Dùng .exists() và .get() để tránh tạo đối tượng Share không cần thiết nếu chỉ cần kiểm tra
            # Nhưng .first() cũng hoạt động tốt và trả về đối tượng nếu có.
            share = self.shares.filter(share_with=user).first()
            if share:
                return share.permission

        if token and self.is_shared_via_link and str(self.share_token) == str(token):
            return self.link_permission

        return None

    def enable_share_link(self, permission='view'):
        # Thêm validation cho permission
        if permission not in ['view', 'edit']:
            raise ValueError("Permission must be 'view' or 'edit'.")
            
        self.is_shared_via_link = True
        self.link_permission = permission
        self.save()
        return self.get_share_link()

    def get_share_link(self):
        return f'{HOST_URL}/notes/by-link/{self.pk}/?token={self.share_token}' # Thay id bằng pk

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
        max_length=10, # Giảm max_length xuống 10
        choices=[('view', 'View'), ('edit', 'Edit')],
        default='view'
    )

    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.title} shared with {self.share_with.username}"