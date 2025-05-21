from django.contrib import admin
from .models import Note, NoteShare, Comment
# Register your models here.
admin.site.register(Note)
admin.site.register(NoteShare)
admin.site.register(Comment)
