import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update a user profile when a new user is saved or an existing
    user is updated.
    """
    if created:
        # If a new user is created, create a new UserProfile.
        UserProfile.objects.get_or_create(user=instance)
        # Generate a 12-digit library card number and save it
        instance.userprofile.library_card_number = generate_library_card_number()
        instance.userprofile.save()
    else:
        # If an existing user is updated, update the existing UserProfile.
        try:
            profile = instance.userprofile
            profile.save()  # Save the existing profile
        except UserProfile.DoesNotExist:
            # If the profile doesn't exist, create a new one.
            UserProfile.objects.create(user=instance)

def generate_library_card_number():
    """
    Generate a random 12-digit library card number.
    """
    return ''.join(random.choices(string.digits, k=12))
