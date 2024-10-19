from django.db import models
from django.contrib.auth.models import AbstractUser
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
    # status = models.ForeignKey(MembershipStatus, on_delete=models.SET_NULL, null=True, blank=True)
