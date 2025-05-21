from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate

def home(request):
    return render(request, 'home/home.html')

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'auth/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                return redirect('home')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'auth/login.html',{'form': form})
