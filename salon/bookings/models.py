from django.contrib.auth.models import User
from django.db import models

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # кто записался
    master = models.ForeignKey(User, related_name='master_bookings', on_delete=models.CASCADE)  # мастер
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()