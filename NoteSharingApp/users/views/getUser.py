# views.py

from django.http import JsonResponse
from django.views import View
from users.service.userService import UserService

class GetUserView(View):
    def get(self, request):
        user_id = request.GET.get("id")
        email = request.GET.get("email")
        name = request.GET.get("name")

        service = UserService()

        if user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return JsonResponse({"error": "Invalid id"}, status=400)

        users = service.get_users(user_id=user_id, email=email, name=name)

        # tìm theo id
        if not hasattr(users, '__iter__') or isinstance(users, UserService().get_users().__class__):
            if users is None:
                return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse({
                "id": users.id,
                "username": users.username,
                "email": users.email
            })

        # Trường hợp là danh sách user
        data = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]
        return JsonResponse(data, safe=False)
