from django.db import models
from django.contrib.auth.models import User
from adminpenal.models import Post, TicketType


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    ground = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookings')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='bookings')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    price_per_ticket = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.ground.title}"
