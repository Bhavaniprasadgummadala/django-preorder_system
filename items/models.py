# items/models.py
from django.db import models
from stalls.models import Stall

class Item(models.Model):
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.price}, {self.preparation_time} mins)"