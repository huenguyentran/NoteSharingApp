from django.urls import include, path
from .views import  GoogleCallbackView, GoogleLoginView, LogoutView, AccountView, UsernameValidationView, PasswordValidationView, CombinedAuthView, CreateAccountValidation, LoginView, RegisterView

urlpatterns = [ 
  path('', CombinedAuthView.as_view(), name='auth_combined'), 
  path('login/google/', GoogleLoginView.as_view(), name='google-login'),
  path('login/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),  
  path('settings/', AccountView.as_view(), name='account_settings'),  
  path('logout/', LogoutView.as_view(), name='logout'), 
    #chinh sua user, xac minh email, doi mat khau

  path('login/', LoginView.as_view(), name='login'),
  path('register/', RegisterView.as_view(), name='register'),
    
  path('username-validation/', UsernameValidationView.as_view() , name='username_validation'),
  path('registration-validation/', CreateAccountValidation.as_view() , name='registration_validation'),
  path('password-validation/',  PasswordValidationView.as_view() , name='password_validation'),
]
