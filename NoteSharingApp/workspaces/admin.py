from django.contrib import admin
from .models import Workspace, WorkspaceMember, WorkspaceFile

# Register your models here.

admin.site.register(Workspace)
admin.site.register(WorkspaceMember)
admin.site.register(WorkspaceFile)