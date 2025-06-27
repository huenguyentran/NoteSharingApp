from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import GetUserView


urlpatterns = [
    #Friend nếu có thể

    #Get user by Id, Email, Name
    #Return: list of user
    path("", GetUserView.as_view(), name="user_query"),
]