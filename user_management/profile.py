# user_management/profile.py
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import random
import string


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True, related_name='userprofile')
    image = models.ImageField(default='default_image/Defaut.png', upload_to='profile_pics')
    address = models.CharField(max_length=400, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    library_card_number = models.CharField(max_length=12, null=True, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Check if the image is not set (empty string)
        if not self.image:
            self.image.name = 'default_image/Defaut.png'
        super().save(*args, **kwargs)

# Use a try-except block to handle the circular import issue
try:
    from user_management.models import User
except ImportError:
    User = None

if User:
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance, library_card_number=generate_library_card_number())

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

def generate_library_card_number():
    """
    Generate a random 12-digit library card number.
    """
    return ''.join(random.choices(string.digits, k=12))