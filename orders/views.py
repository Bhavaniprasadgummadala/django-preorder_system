from django.utils.timezone import timezone  # Change this import
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.timesince import timesince  # Add this import
from stalls.models import Stall
from .models import Order
from items.models import Item
from django.http import JsonResponse

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['quantity']
    template_name = 'orders/order_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(id=self.kwargs['item_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # Critical line
        form.instance.item = get_object_or_404(Item, id=self.kwargs['item_id'])
        messages.success(self.request, "Order placed successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('order_success', kwargs={'pk': self.object.id})

class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['order'] = Order.objects.get(
                id=self.kwargs['pk'],
                user=self.request.user
            )
        except Order.DoesNotExist:
            messages.error(self.request, "Order not found")
        return context

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all available stalls with their items
        context['stalls'] = Stall.objects.filter(
            items__available=True
        ).distinct().prefetch_related(
            'items'
        ).order_by('name')
        
        # Get user's orders if authenticated - ADD CACHE CONTROL
        if self.request.user.is_authenticated:
            context['orders'] = Order.objects.filter(
                user=self.request.user
            ).select_related(
                'item', 
                'item__stall'
            ).order_by('-created_at')[:5]
            # Force fresh query
            context['orders']._result_cache = None
        
        return context

class CustomerOrderView(LoginRequiredMixin, ListView):
    template_name = 'orders/customer_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at').select_related('item', 'item__stall')

class StallOrdersView(LoginRequiredMixin, ListView):
    """View for stall owners to see their orders"""
    template_name = 'orders/stall_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            item__stall__user=self.request.user
        ).order_by('-created_at').select_related('item', 'user')

class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at').select_related('item', 'item__stall')
    
class UserOrdersView(LoginRequiredMixin, ListView):
    template_name = 'orders/user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        # Only show orders for the currently logged-in user
        return Order.objects.filter(
            user=self.request.user
        ).select_related('item', 'item__stall').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'orders'  # For highlighting nav menu
        return context
    
def get_recent_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
        orders_data = []
        for order in orders:
            orders_data.append({
                'item_name': order.item.name,
                'stall_name': order.item.stall.name,
                'price': str(order.item.price),
                'time_ago': timesince(order.created_at),  # Use timesince here
                'status': order.status,
                'status_display': order.get_status_display(),
                'status_class': 'success' if order.status == 'COMPLETED' else 'warning',
                'quantity': order.quantity
            })
        return JsonResponse({'orders': orders_data})
    return JsonResponse({'orders': []})