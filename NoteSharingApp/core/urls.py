from django.urls import path
from .views import HomeView

urlpatterns = [ 
  path('', HomeView.as_view(), name='home'),
  path('error/', HomeView.as_view(), name='error_view'),
]
