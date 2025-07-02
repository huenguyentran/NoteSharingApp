from django.http import JsonResponse
from django.views import View
from users.service.userService import UserService

class GetUserView(View):
    def get(self, request):
        print("➡️ GetUserView was called")
        user_id = request.GET.get("id")
        name = request.GET.get("name")
        email = request.GET.get("email")

        service = UserService()

        try:
            if user_id:
                user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid user id"}, status=400)

        users = service.get_users(user_id=user_id, name=name, email=email)

        if not users:
            return JsonResponse([], safe=False)

        # Trường hợp chỉ 1 user (không phải list)
        if not isinstance(users, list) and not hasattr(users, "__iter__"):
            return JsonResponse({
                "id": users.id,
                "username": users.username,
                "email": users.email
            })

        # Trường hợp là danh sách
        result = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]
        return JsonResponse(result, safe=False)
