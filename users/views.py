from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from stalls.models import Stall

class HomeView(ListView):
    template_name = 'users/home.html' 
    context_object_name = 'stalls'
    
    def get_queryset(self):
        # Get stalls that have at least one available item
        return Stall.objects.filter(
            items__available=True
        ).distinct().prefetch_related(
            'items'
        ).filter(
            items__isnull=False  # Ensure stalls have items
        )

class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'users/profile.html'
    context_object_name = 'stalls'
    
    def get_queryset(self):
        if self.request.user.user_type == 'S':
            return Stall.objects.filter(owner=self.request.user)
        return Stall.objects.none()  # Return empty for regular users