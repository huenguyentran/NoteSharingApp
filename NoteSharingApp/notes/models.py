from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField()              
    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes'
    )  
    # Người tạo ghi chú (ForeignKey đến User)

    group_id = models.IntegerField(
        null=True,
        blank=True
    )  
    # ID nhóm (có thể NULL nếu là ghi chú cá nhân)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True)    

    def __str__(self):
        return self.title