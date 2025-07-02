from django.db import models
from django.contrib.auth.models import User
from notes.models import Note # Đảm bảo bạn đã import Note model nếu cần

class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    parent_comment = models.ForeignKey(
        'self', # 'self' để tham chiếu đến chính model Comment
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies' # Tên reverse access từ comment cha đến các comment con
    )

    def __str__(self):
        return f"Comment by {self.user.username} on {self.note.title}"

    class Meta:
        # Bạn có thể thêm order_by mặc định nếu muốn
        ordering = ['-created_at']