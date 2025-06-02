from django.views import View
from urllib.parse import urlencode
from django.shortcuts import redirect
from dotenv import load_dotenv
load_dotenv()

import os
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

class GoogleLoginView(View):
  def get(self, request):
    base_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:8000/login/google/callback/",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)