from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UserService:
    def get_user(self, *, user_id=None, email=None, name=None):
        """
        Tìm user theo:
        - id (nếu có)
        - hoặc email__icontains & username__icontains
        - hoặc chỉ email__icontains
        - hoặc chỉ username__icontains
        """
        if user_id is not None:
            return User.objects.filter(id=user_id).first()

        if email and name:
            return User.objects.filter(
                Q(email__icontains=email) & Q(username__icontains=name)
            )

        if email:
            return User.objects.filter(email__icontains=email)

        if name:
            return User.objects.filter(
                Q(firstname__icontains=name) | Q(lastname__icontains=name)
            ) 

        return None

