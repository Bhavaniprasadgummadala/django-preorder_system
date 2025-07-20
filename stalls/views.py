from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Stall
from orders.models import Order
from items.models import Item  # Import Item model if needed for relationships

class StallCreateView(LoginRequiredMixin, CreateView):
    model = Stall
    fields = ['name', 'description']
    template_name = 'stalls/stall_form.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Stall created successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('stall_dashboard')

class StallUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Stall
    fields = ['name', 'description']
    template_name = 'stalls/stall_form.html'
    
    def test_func(self):
        stall = self.get_object()
        return stall.owner == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Stall updated successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('stall_dashboard')

class StallDashboardView(LoginRequiredMixin, ListView):
    model = Stall
    template_name = 'stalls/dashboard.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return Stall.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all orders for all stalls owned by this user
        context['orders'] = (
            Order.objects.filter(item__stall__owner=self.request.user)
            .select_related('item', 'user', 'item__stall')
            .order_by('-created_at')[:10]  # Show last 10 orders
        )
        
        return context
class StallOrdersView(LoginRequiredMixin, ListView):
    template_name = 'stalls/order_management.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        # Verify the stall belongs to the current user
        stall = get_object_or_404(
            Stall, 
            id=self.kwargs['stall_id'],
            owner=self.request.user
        )
        return (
            Order.objects.filter(item__stall=stall)
            .select_related('item', 'user')
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stall'] = get_object_or_404(
            Stall, 
            id=self.kwargs['stall_id'],
            owner=self.request.user
        )
        return context

class UpdateOrderStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, status):
        order = get_object_or_404(Order, pk=pk)
        
        # Verify the order belongs to the user's stall
        if order.item.stall.owner != request.user:
            messages.error(request, "You don't have permission to update this order")
            return redirect('stall_dashboard')

        # Validate status
        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if status not in valid_statuses:
            messages.error(request, "Invalid order status")
            return redirect('stall_orders', stall_id=order.item.stall.id)

        # Update status
        order.status = status
        if status == 'COMPLETED':
            order.completed_at = timezone.now()
        order.save()

        messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}")
        return redirect('stall_orders', stall_id=order.item.stall.id)