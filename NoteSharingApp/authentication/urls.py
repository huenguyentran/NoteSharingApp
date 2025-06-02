from django.urls import include, path
from .views import LoginView, RegistrationView, HomeView, GoogleCallbackView, GoogleLoginView, LogoutView, AccountView
urlpatterns = [ 
  path('', HomeView.as_view(), name='home'),
  path('login/', LoginView.as_view(), name='login'),
  path('login/google/', GoogleLoginView.as_view(), name='google-login'),
  path('login/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
  path('register/', RegistrationView.as_view(), name='registration'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('settings/', AccountView.as_view(), name='account_settings'),  
  #chinh sua user, xac minh email, doi mat khau
]
