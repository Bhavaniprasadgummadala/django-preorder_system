from django.urls import path
from .views import (
    StallCreateView,
    StallUpdateView,
    StallDashboardView,
    StallOrdersView,
    UpdateOrderStatusView
)

urlpatterns = [
    path('create/', StallCreateView.as_view(), name='stall_create'),
    path('<int:pk>/update/', StallUpdateView.as_view(), name='stall_update'),
    path('dashboard/', StallDashboardView.as_view(), name='stall_dashboard'),
    # Changed to use stall_id parameter
    path('<int:stall_id>/orders/', StallOrdersView.as_view(), name='stall_orders'),
    path('orders/<int:pk>/update-status/<str:status>/', 
         UpdateOrderStatusView.as_view(), 
         name='update_order_status'),
]