from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    
    def __str__(self):
        return self.title


class TicketType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price', 'name']

    def __str__(self):
        return f"{self.name} - Rs. {self.price}"
