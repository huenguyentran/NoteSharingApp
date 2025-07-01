from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),
    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('workspaces/', include('workspaces.urls')),
    path('api/comments/', include('comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
