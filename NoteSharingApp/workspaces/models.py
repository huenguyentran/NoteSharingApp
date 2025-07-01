from django.db import models
from django.utils import timezone

# Create your models here.
def workspace_uploadThumb_path(instance, filename):
    return f'workspace_files/{instance.id}/{filename}_{timezone.now().strftime("%Y%m%d%H%M%S")}'

class Workspace(models.Model):
    name = models.CharField(max_length=200)  

    thumbnail = models.ImageField(upload_to=workspace_uploadThumb_path, blank=True, null=True)   
    description = models.TextField()       

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


    
class WorkspaceMember(models.Model):
    class Meta:
        unique_together = ('workspace', 'user')

    workspace = models.ForeignKey(
        Workspace, 
        on_delete=models.CASCADE,
        related_name='members'
    )

    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE,
        related_name='workspace_memberships'
    )

    permission = models.CharField(
        max_length=10,
        choices=[('view', 'View'), ('edit', 'Edit')],
        default='view'
    )

    isAdmin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username + " in " + self.workspace.name    
    

class WorkspaceFile(models.Model):
    workspace = models.ForeignKey(
        Workspace, 
        on_delete=models.CASCADE
    )

    def workspace_upload_path(instance, filename):
        return f'workspace_files/{instance.workspace.id}/{filename}'

    file = models.FileField(upload_to=workspace_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.file.name