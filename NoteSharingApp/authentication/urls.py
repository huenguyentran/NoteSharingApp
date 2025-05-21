from django.urls import include, path
from . import views

urlpatterns = [ 
  path('', views.home, name='home'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.login_view, name='logout'),
]
