from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    #otp = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    #is_mobile_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']




class booking(models.Model):

    pickup_city = models.CharField(max_length=100,default='')
    drop_city = models.CharField(max_length=100,default='')
    pickup_address = models.CharField(max_length=200)
    drop_address = models.CharField(max_length=200)
    mobile_b = models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=50)



    def save(self, *args, **kwargs):
        # Check if a user with the provided email already exists
        user = User.objects.filter(email=self.email).first()

        existing_user = User.objects.filter(mobile=self.mobile_b).first()

        if not user and not existing_user:
            # If no user exists with the provided email and mobile number, create a new user
            username = self.name  # Set the username as the mobile number
            mobile = self.mobile_b  # Generate a random password
            email = self.email

            user = User.objects.create_user(username=username, email=email, mobile=mobile)
            user.save()

        super().save(*args, **kwargs)



    def __str__(self):
        return self.name





