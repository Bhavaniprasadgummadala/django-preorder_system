from django.urls import reverse_lazy
from django import forms
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError


User = get_user_model()
@method_decorator(never_cache, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        
        # 1. Completely clear existing session
        self.request.session.flush()
        
        # 2. Create new session BEFORE login
        self.request.session.create()
        self.request.session.save()
        
        # 3. Explicit login with session save
        login(self.request, user)
        self.request.session['_auth_user_hash'] = self.request.user.get_session_auth_hash()
        self.request.session.save()  # Force immediate save
        
        # 4. Verify session in database
        from django.contrib.sessions.models import Session
        print(f"Session exists in DB: {Session.objects.filter(session_key=self.request.session.session_key).exists()}")
        
        # 5. Create response with cache control
        response = self.get_success_response()
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Fri, 31 Dec 1999 23:59:59 GMT'
        
        # 6. Add small delay to ensure session persistence
        import time
        time.sleep(0.5)  # Only for debugging - remove in production
        
        return response
    
    def get_success_response(self):
        user = self.request.user
        try:
            if user.user_type == 'S':
                return redirect('stall_dashboard')
            return redirect(self.get_success_url())
        except Exception as e:
            print(f"Redirect error: {str(e)}")
            return redirect('home')
    
class CustomLogoutView(LogoutView):
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        # Debug before logout
        print(f"\n=== PRE-LOGOUT DEBUG ===")
        print(f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        print(f"Session Key: {request.session.session_key if hasattr(request, 'session') else 'No session'}")
        
        response = super().dispatch(request, *args, **kwargs)
        
        # Debug after logout
        print(f"\n=== POST-LOGOUT DEBUG ===")
        print(f"Session cleared: {not hasattr(request, 'session') or not request.session.session_key}")
        print("=======================\n")
        
        messages.info(request, "You have been logged out successfully.")
        return response

User = get_user_model()


def check_session(request):
    """Enhanced session check endpoint with more debugging info"""
    session_info = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'user_type': getattr(request.user, 'user_type', None) if request.user.is_authenticated else None,
        'session_key': request.session.session_key if hasattr(request, 'session') else None,
        'session_expiry': request.session.get_expiry_age() if hasattr(request, 'session') else None,
        'session_user_id': request.session.get('_auth_user_id') if hasattr(request, 'session') else None
    }
    
    # Debug output
    print(f"\n=== SESSION CHECK ===")
    print(f"Session exists: {hasattr(request, 'session')}")
    print(f"Session key: {session_info['session_key']}")
    print(f"Authenticated: {session_info['authenticated']}")
    print(f"User: {session_info['username']}")
    print(f"User type: {session_info['user_type']}")
    print("====================\n")
    
    return JsonResponse(session_info)

class RegistrationView(CreateView):
    form_class = UserRegistrationForm  # Points to your form
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')  # Redirect after success

    def form_valid(self, form):
        try:
            user = form.save()  # Calls save() from UserRegistrationForm
            if user:  # Check if user was created
                messages.success(
                    self.request, 
                    "Registration successful! Please log in."
                )
                return super().form_valid(form)
            else:
                raise ValueError("Form.save() returned None")
                
        except Exception as e:
            messages.error(
                self.request,
                f"Registration failed: {str(e)}"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Debugging
        return super().form_invalid(form)
