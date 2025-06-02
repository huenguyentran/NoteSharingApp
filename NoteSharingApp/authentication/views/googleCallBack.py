from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from dotenv import load_dotenv
import requests
load_dotenv()

import os
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


class GoogleCallbackView(View):
  def get(self, request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("No code provided.")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/login/google/callback/",
        "grant_type": "authorization_code"
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return HttpResponse("Access token not received.")

    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        return HttpResponse("Google không trả về email.")

    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": name.split()[0] if name else '',
            "last_name": ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else ''
        }
    )
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return redirect('/')