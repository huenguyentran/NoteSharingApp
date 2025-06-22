from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from notes.models import Note

    
    
class Comment(models.Model):
    note = models.ForeignKey(
        Note, 
        null=True,
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

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.note.title}"