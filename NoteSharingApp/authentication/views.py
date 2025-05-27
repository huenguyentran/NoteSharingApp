from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from notes.models import Note
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from urllib.parse import urlencode
from django.contrib.auth.models import User
from dotenv import load_dotenv
load_dotenv()

import os
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

def home(request):
    

    if not request.user.is_authenticated:
        return redirect('login')
    else:
        deleted_notes = Note.objects.filter(create_by=request.user, deleted_at__isnull = False)
        notes = Note.objects.filter(create_by=request.user, deleted_at__isnull = True) 
        return render(request, 'home/home.html', {'notes': notes})

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'accounts/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                return redirect('home')
        
        messages.error(request,f'Invalid username or password')
        return render(request,'auth/login.html',{'form': form})


def google_login(request):
    base_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": client_id,
        "redirect_uri": "http://127.0.0.1:8000/login/google/callback/",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)



def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("No code provided.")

    # Đổi code sang access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://127.0.0.1:8000/login/google/callback/",
        "grant_type": "authorization_code"
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    # Lấy thông tin user
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        return HttpResponse("Google không trả về email.")
    # Tạo user nếu chưa có
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": name.split()[0] if name else '',
            "last_name": ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else ''
        }
    )
    # Đăng nhập user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    # Chuyển về home
    return redirect('/')

