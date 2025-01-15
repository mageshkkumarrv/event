# events/models.py
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('movies', 'Movies'),
        ('sports', 'Sports'),
        ('theatre', 'Theatre'),
        ('comedy', 'Comedy'),
        ('conference', 'Conference'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_tickets = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    event = models.ForeignKey(Event, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15, null=True, blank=True)  
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.event.name}"
