from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', default='default.png', null=True,)

    def __str__(self):
        return f'{self.user.username} Profile'
