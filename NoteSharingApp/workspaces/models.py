from django.db import models

# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=200)  
    description = models.TextField()          
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.name
    
class WorkspaceMember(models.Model):
    workspace = models.ForeignKey(
        Workspace, 
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE
    )

    isAdmin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    permission = models.CharField(
        max_length=50, 
        choices=[('view', 'View'), ('edit', 'Edit')], 
        default='view'
    )

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