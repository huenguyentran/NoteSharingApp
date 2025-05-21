from django.contrib import messages
from django.shortcuts import render, redirect
from notes.models import Note
from .forms import LoginForm
from django.contrib.auth import login, authenticate

def home(request):
    deleted_notes = Note.objects.filter(create_by=request.user, deleted_at__isnull = False)
    notes = Note.objects.filter(create_by=request.user, deleted_at__isnull = True) 
    return render(request, 'home/home.html', {'notes': notes})

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
        
        messages.error(request,f'Invalid username or password')
        return render(request,'auth/login.html',{'form': form})
