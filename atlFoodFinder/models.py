from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, unique=True)
    rating = models.FloatField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} favorited by {self.user.username}"