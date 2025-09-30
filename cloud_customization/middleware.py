import os
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User


class AutoAdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login')  # Make sure your login url name is 'login'
        if (
            request.path == login_url
            and not request.user.is_authenticated
            and request.method == "GET"
        ):
            admin_email = os.environ.get("HORILLA_ADMIN_EMAIL")
            admin_password = os.environ.get("HORILLA_ADMIN_PASSWORD")
            if admin_email and admin_password: 
                user = User.objects.filter(is_superuser=True, username=admin_email).first()
                user.is_active = True
                user.save()
                user = authenticate(request, username=admin_email, password=admin_password)
                if user is not None:
                    if user.last_login is None: 
                        login(request, user)
                        return redirect('/')  # Redirect to home or any page you want
        return self.get_response(request)