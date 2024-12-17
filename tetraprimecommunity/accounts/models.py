from typing import Dict, Any
from django.db import models
from typing import TYPE_CHECKING
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Manager
from django.utils.functional import empty
from wagtail.admin.panels import FieldPanel
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import os


def get_default_preferences():
    return {
        "bio_intro": '',                            # Bio introduction
        "bio_current_professional_title": '',       # Current Professional Title
        "bio_top_technical_skills": '',             # Top technical skills
        "bio_relevant_certifications": '',          # Relevant certifications
        "bio_favorite_tools_and_technologies": '',  # Favorite Tools & Technologies
        "bio_career_goals": '',                     # Career Goals
        "bio_dream_project": '',                    # Dream Project
        "bio_projects_youre_proud_of": '',          # Projects You're Proud of
        "bio_areas_for_growth": '',                 # Areas for Growth
        "bio_open_for_collaboration_on": '',        # Open for Collaboration On
        "bio_seeking_a_mentor": '',                 # Seeking a Mentor
        "bio_open_to_mentoring_others": '',         # Open to Mentoring Others
        "bio_need_help_with": '',                   # Need Help With
        "bio_favorite_quote": '',                   # Favorite Quote
        "bio_superpower": '',                       # Superpower
        "bio_first_experience_in_tech": '',         # First Experience in Tech
        "bio_hobbies_and_passions": '',             # Hobbies & Passions
        "private_profile": False,                   # Hide profile from Discovery and Search
        "dark_mode": False,                         # Dark / Light mode setting
        "email_notifications": False,               # Get email alerts
        "language": "en",                           # Choose default language
        "onboarding": True,                         # Onboarding visible or not
        "onboarding_complete": False,                # Onboarding was completed a single time
    }


def validate_image_file_type(value):
    """Ensure the uploaded file is an image with a valid extension."""
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed: {", ".join(valid_extensions)}')


def validate_image_file_size(value):
    """Ensure the uploaded image is below the size limit."""
    max_file_size = 600 * 1024  # 600 KB
    if value.size > max_file_size:
        raise ValidationError(f'File size exceeds the limit of 600 KB.')


class CustomUser(AbstractUser):
    country = models.CharField(verbose_name='country', max_length=50)
    profile_picture = models.ImageField(upload_to='users/profile_pictures/', blank=True, null=True, validators=[validate_image_file_type, validate_image_file_size])
    banner_image = models.ImageField(upload_to='users/banner_images/', blank=True, null=True, validators=[validate_image_file_type, validate_image_file_size])
    preferences = models.JSONField(default=get_default_preferences, blank=True)

    def set_preference(self, key, value):
        """Set a user preference."""
        self.preferences[key] = value
        self.save()

    def get_preference(self, key, default=None):
        """Retrieve a user preference."""
        return self.preferences.get(key, default)

    def remove_preference(self, key):
        """Remove a user preference."""
        if key in self.preferences:
            del self.preferences[key]
            self.save()

    def profile_completion_status(self):
        """Calculate profile completion percentage and missing fields."""
        GROUPED_PREFERENCES_FIELDS = {
            'Professional Overview': ['bio_current_professional_title', 'bio_top_technical_skills', 'bio_relevant_certifications', 'bio_favorite_tools_and_technologies'],
            'Aspirations & Projects': ['bio_career_goals', 'bio_dream_project', 'bio_projects_youre_proud_of', 'bio_areas_for_growth'],
            'Collaboration & Teams': ['bio_open_for_collaboration_on', 'bio_seeking_a_mentor', 'bio_open_to_mentoring_others', 'bio_need_help_with'],
            'Personality & Interests': ['bio_favorite_quote', 'bio_superpower', 'bio_first_experience_in_tech', 'bio_hobbies_and_passions'],
        }

        completed_groups = []
        incomplete_groups = []

        # Evaluate each group
        for group_name, fields in GROUPED_PREFERENCES_FIELDS.items():
            if all(self.preferences.get(field) for field in fields):  # Check if all fields in the group have values
                completed_groups.append(group_name)
            else:
                incomplete_groups.append(group_name)

        total_groups = len(GROUPED_PREFERENCES_FIELDS)
        completed = len(completed_groups)

        # Update onboarding_complete preference based on completion status
        onboarding_complete = total_groups == completed
        self.set_preference('onboarding_complete', onboarding_complete)

        return {
            'completed_groups': completed_groups,
            'incomplete_groups': incomplete_groups,
            'total_groups': total_groups,
            'percentage': (completed / total_groups) * 100,
        }


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
