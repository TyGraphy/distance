from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    username = None
    mobile_number = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []


class booking(models.Model):
    pickup_city = models.CharField(max_length=100,default='')
    drop_city = models.CharField(max_length=100,default='')
    pickup_address = models.CharField(max_length=200)
    drop_address = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()




    def __str__(self):
        return self.name





