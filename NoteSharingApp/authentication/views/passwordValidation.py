import json
import re
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User


import json
import re
from django.http import JsonResponse
from django.views import View

class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        if not str(password).isalnum():
            return JsonResponse({'password_error': 'Mật khẩu chỉ được chứa chữ cái và số.'})
        if len(password) < 6:
            return JsonResponse({'password_error': 'Mật khẩu phải có ít nhất 6 ký tự.'})
        if len(password) > 30:
            return JsonResponse({'password_error': 'Mật khẩu không được vượt quá 30 ký tự.'})
        if not re.search(r"[A-Z]", password):
            return JsonResponse({'password_error': 'Mật khẩu phải chứa ít nhất một chữ cái viết hoa.'})
        if not re.search(r"[a-z]", password):
            return JsonResponse({'password_error': 'Mật khẩu phải chứa ít nhất một chữ cái thường.'})
        if not re.search(r'\d', password):
            return JsonResponse({'password_error': 'Mật khẩu phải chứa ít nhất một chữ số.'})

        return JsonResponse({'password_valid': True})
