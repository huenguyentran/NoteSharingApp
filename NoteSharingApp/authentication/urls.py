from django.urls import include, path
from . import views

urlpatterns = [ 
  path('', views.home, name='home'),
  path('login/', views.login_view, name='login'),
  path('login/google/', views.google_login, name='google-login'),
  path('login/google/callback/', views.google_callback, name='google_callback'),
  path('register/', views.registration, name='registration'),
  path('logout/', views.login_view, name='logout'),
]
