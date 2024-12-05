from typing import Dict, Any
from django.db import models
from typing import TYPE_CHECKING
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Manager
from wagtail.admin.panels import FieldPanel

# Define choices for MembershipStatus
# MEMBERSHIP_STATUS_CHOICES = [
#     ('active', 'Active'),
#     ('inactive', 'Inactive'),
#     ('suspended', 'Suspended'),
#     ('pending', 'Pending'),
#     ('banned', 'Banned'),
#     ('guest', 'Guest'),
#     ('verified', 'Verified'),
#     ('trial', 'Trial'),
#     ('expired', 'Expired'),
#     ('premium', 'Premium'),
#     ('restricted', 'Restricted'),
# ]


# MembershipStatus model, which will act as a ForeignKey reference
# class MembershipStatus(models.Model):
#     name = models.CharField(max_length=15, choices=MEMBERSHIP_STATUS_CHOICES, default='active', unique=True)
#     description = models.TextField(blank=True, null=True)


class CustomUser(AbstractUser):
    country = models.CharField(verbose_name='country', max_length=50)
    profile_picture = models.ImageField(upload_to='users/profile_pictures/', blank=True, null=True)

    # status = models.ForeignKey(MembershipStatus, on_delete=models.SET_NULL, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.profile_picture:
    #         print(f"Before Save - File Path: {self.profile_picture.path}")
    #         print(f"Before Save - File URL: {self.profile_picture.url}")
    #     super().save(*args, **kwargs)  # Call the default save method
    #     if self.profile_picture:
    #         print(f"After Save - File Path: {self.profile_picture.path}")
    #         print(f"After Save - File URL: {self.profile_picture.url}")


# if TYPE_CHECKING:
#     from django.contrib.auth.models import AbstractUser
#
#
# class Preferences(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='preferences'
#     )
#     settings = models.JSONField(default=dict)  # Store preferences as a JSONField
#
#     # Type hints for IDE clarity
#     user: "AbstractUser"
#     settings: Dict[str, Any]
#
#     objects: Manager = models.Manager()
#
#     def __str__(self):
#         return f"{self.user.username}'s Preferences"
#
#     # Helper methods
#     def get_preference(self, key, default=None):
#         """Retrieve a specific preference."""
#         return self.settings.get(key, default)
#
#     def set_preference(self, key, value):
#         """Set or update a specific preference."""
#         self.settings[key] = value
#         self.save()
