import json
import re
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User


class CreateAccountValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']
        confirm_password = data['confirmPassword']
        
        if password != confirm_password:
            return JsonResponse({'validation_error': 'Mật khẩu xác nhận không khớp.'})

        return JsonResponse({})
        