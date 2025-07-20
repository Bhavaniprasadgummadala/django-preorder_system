# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        if self.request.user.user_type == 'S':
            try:
                return reverse_lazy('stall_dashboard')  # No namespace
            except:
                return reverse_lazy('home')  # Fallback
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = 'home'

class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')