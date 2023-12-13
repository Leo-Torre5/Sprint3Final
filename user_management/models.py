# user_management/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_management.profile import UserProfile
from django.contrib.auth import get_user_model




@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Add unique related_name attributes to avoid clashes
get_user_model()._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
get_user_model()._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_user_permissions'

# Add a property to access the user profile
@property
def user_profile(self):
    try:
        return self.userprofile
    except UserProfile.DoesNotExist:
        return None

get_user_model().add_to_class('user_profile', user_profile)
