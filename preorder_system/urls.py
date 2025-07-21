# project_name/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Apps
    path('accounts/', include('accounts.urls')),
    path('stalls/', include('stalls.urls')),
    path('', include('users.urls')),
    path('items/', include('items.urls')),
    path('orders/', include('orders.urls')),
]