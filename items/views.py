from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Item
from stalls.models import Stall

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['name', 'preparation_time', 'price', 'available']  # Updated fields
    template_name = 'items/item_form.html'

    def form_valid(self, form):
        form.instance.stall = Stall.objects.get(id=self.kwargs['stall_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('stall_dashboard')

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'preparation_time', 'price', 'available']
    template_name = 'items/item_form.html'
    
    def get_success_url(self):
        return reverse_lazy('stall_dashboard')
    
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('stall_dashboard')