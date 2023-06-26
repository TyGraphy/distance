from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Amenities)
admin.site.register(Car)
admin.site.register(car_image)
admin.site.register(CarBooking)
admin.site.register(booking)

