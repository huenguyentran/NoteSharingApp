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
            return JsonResponse({'username_error': 'Username can only contain letters and numbers.'})
        
        if len(username) < 6:
            return JsonResponse({'username_error': 'Username must be at least 6 characters long.'})
        
        if len(username) > 30:
            return JsonResponse({'username_error': 'Username cannot exceed 30 characters.'})
        
        if not re.search(r'[A-Za-z]', username):
            return JsonResponse({'username_error': 'Username must contain at least one letter.'})
        
        if not re.search(r'\d', username):
            return JsonResponse({'username_error': 'Username must contain at least one digit.'})
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'This username is already taken, please choose another.'})
            
        return JsonResponse({'username_valid': True})