from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Preferences


DEFAULT_PREFERENCES = {
    'theme': 'light',
    'notifications': True,
    'language': 'en',
}


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_preferences(sender, instance, created, **kwargs):
#     if created:
#         print(f"Creating Preferences for user {instance.username}")
#         Preferences.objects.create(user=instance, settings=DEFAULT_PREFERENCES)
