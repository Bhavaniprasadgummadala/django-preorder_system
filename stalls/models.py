from django.db import models
from accounts.models import CustomUser  # Only direct import needed

class Stall(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def recent_orders(self):
        from orders.models import Order
        return Order.objects.filter(item__stall=self).select_related('item', 'user').order_by('-created_at')[:5]
