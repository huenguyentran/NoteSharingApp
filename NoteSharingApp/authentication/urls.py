from django.urls import include, path
from .views import HomeView, GoogleCallbackView, GoogleLoginView, LogoutView, AccountView, CombinedAuthView # THAY ĐỔI DÒNG NÀY

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('auth/', CombinedAuthView.as_view(), name='auth_combined'), 

    path('login/google/', GoogleLoginView.as_view(), name='google-login'),
    path('login/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', AccountView.as_view(), name='account_settings'),   
    #chinh sua user, xac minh email, doi mat khau
]