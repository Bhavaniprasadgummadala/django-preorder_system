from django.urls import path
from .views import ItemCreateView, ItemUpdateView, ItemDeleteView  # Add ItemUpdateView

urlpatterns = [
    path('<int:stall_id>/create/', ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/edit/', ItemUpdateView.as_view(), name='item_update'),
    path('<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
  # Add this line
]