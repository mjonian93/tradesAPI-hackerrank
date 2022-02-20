from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trade(models.Model):
    type = models.CharField(max_length=10, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, blank=False)
    shares = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)