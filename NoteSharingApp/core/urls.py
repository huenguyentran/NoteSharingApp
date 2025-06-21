from django.urls import path
from .views import DashBoardView
from .views.ErrorView import ErrorView
urlpatterns = [ 
  path('', DashBoardView.as_view(), name='dashboard'),
  path('error/', ErrorView, name='error_view'),
]
