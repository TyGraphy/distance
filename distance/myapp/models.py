from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save








class Amenities(models.Model):
    amenity_name = models.CharField(max_length=100)


    def __str__(self):
        return self.amenity_name




class Car(models.Model):
    car_name = models.CharField(max_length=100)
    trip_price = models.IntegerField()
    amenities = models.ManyToManyField(Amenities)
    type = models.CharField(max_length=100)
    seat = models.IntegerField()
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.car_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("cab_list", kwargs={'slug': self.slug})

    class Meta:
        db_table = "myapp_Car"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.car_name)
    if new_slug is not None:
        slug = new_slug
    qs = Car.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Car)




class car_image(models.Model):
    cars_i = models.ForeignKey(Car, related_name="car_images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="car")



class CarBooking(models.Model):
    cars = models.ForeignKey(Car, related_name="car_booking", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_booking", on_delete=models.CASCADE)
    pickup = models.CharField(max_length=100)
    drop = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    payment = models.IntegerField()
    payment_type = models.CharField(choices=(('half', 'half'),('full','full')), max_length=100)



#class First(models.Model):
    #origin = models.CharField(max_length=500)
    #destination = models.CharField(max_length=500)
    #date = models.DateField(null=True)
    #time = models.TimeField(null=True)


class booking(models.Model):
    pickup_city = models.CharField(max_length=100,default='')
    drop_city = models.CharField(max_length=100,default='')
    pickup_address = models.CharField(max_length=200)
    drop_address = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()
    altmobile = models.IntegerField()
    gst = models.CharField(max_length=100)
    remark = models.TextField(null=True)


    def __str__(self):
        return self.name




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=100)
    otp = models.CharField(max_length=100, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
