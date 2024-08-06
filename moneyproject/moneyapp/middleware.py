from django.shortcuts import redirect
from django.urls import reverse

class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):  # Check if the path is admin panel
            if not request.user.is_superuser:  # Check if the user is not a superuser
                return redirect('login')  # Redirect to login or any other page
        response = self.get_response(request)
        return response
