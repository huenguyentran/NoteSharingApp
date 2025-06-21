from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
class LogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect('auth_combined')