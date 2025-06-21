import json
import re
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return  JsonResponse({'username_error': 'Tên đăng nhập chỉ được chứa chữ cái và số.'})
        if len(username) < 6:
            return JsonResponse({'username_error': 'Tên đăng nhập phải có ít nhất 6 ký tự.'})
        if len(username) > 30:
            return JsonResponse({'username_error': 'Tên đăng nhập không được vượt quá 30 ký tự.'})
        if not re.search(r'[A-Za-z]', username):
            return JsonResponse({'username_error': 'Tên đăng nhập phải chứa ít nhất một chữ cái.'})
        if not re.search(r'\d', username):
            return JsonResponse({'username_error': 'Tên đăng nhập phải chứa ít nhất một chữ số.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.'})
        return JsonResponse({'username_valid': True})
        