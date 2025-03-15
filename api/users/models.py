from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    phone = models.CharField(max_length=15, blank=True, null=True)
    addressLine1 = models.CharField(max_length=50, blank=True, null=True)
    addressLine2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postalCode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, null=True, default="Egypt")

    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', null=True,)


    def __str__(self):
        return f'{self.user.username} Profile'
