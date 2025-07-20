from django.db import models
from accounts.models import CustomUser
from items.models import Item

# orders/models.py
from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready for Pickup'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    pickup_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.item.name}"
    
    def estimated_ready_time(self):
        if self.status == 'PREPARING':
            return self.created_at + timezone.timedelta(minutes=self.item.preparation_time)
        return None