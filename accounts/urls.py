# accounts/urls.py
from django.urls import path
from .views import RegistrationView, CustomLoginView, CustomLogoutView, check_session

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('check_session/', check_session, name='check_session'),
]

