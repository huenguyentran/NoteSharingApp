# D:\Learning\REPO_GITHUB\NoteSharingApp\NoteSharingApp\workspaces\admin.py

from django.contrib import admin
from .models import Workspace, WorkspaceMember, WorkspaceFile # Đảm bảo dòng này đúng

# Register your models here.
admin.site.register(Workspace)
admin.site.register(WorkspaceMember)
admin.site.register(WorkspaceFile)