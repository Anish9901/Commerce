from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class bids(models.Model):
    current_price = models.DecimalField(max_digits=100,decimal_places=2) #change hote rahega
    def __str__(self):
        return f"{self.current_price}" 

class listings(models.Model):
    lister = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    item_name = models.CharField(max_length=64)
    description = models.TextField()
    url = models.URLField()
    category = models.CharField(max_length=64)
    price = models.ForeignKey(bids,on_delete=models.CASCADE,name="price")
    def __str__(self):
        return f"{self.pk} {self.item_name} {self.description} {self.price} {self.category}"

class watchlist(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    item = models.ForeignKey(listings,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.users} {self.item}"
        
class comments:
    comments = models.CharField()

class auction_categories:
    
    pass

