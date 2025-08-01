from django.urls import path
from . import views  
from .views import (
    OrderCreateView,
    OrderSuccessView,
    OrderHistoryView,
    UserOrdersView,
    StallOrdersView
)

urlpatterns = [
    path('history/', OrderHistoryView.as_view(), name='order_history'),
    path('my-orders/', UserOrdersView.as_view(), name='user_orders'),
    path('<int:pk>/success/', OrderSuccessView.as_view(), name='order_success'),
    path('<int:item_id>/create/', OrderCreateView.as_view(), name='order_create'),
    path('stall-orders/', StallOrdersView.as_view(), name='stall_orders'),
    path('get-recent-orders/', views.get_recent_orders, name='get_recent_orders'),
]