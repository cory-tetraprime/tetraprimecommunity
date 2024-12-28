from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import os

User = get_user_model()


def get_default_preferences():
    return {
        "status": 'draft',  # Bio introduction
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


class Project(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('moderation', 'Moderation'),
        ('archived', 'Archived'),
        ('trash', 'Trash'),
    ]

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='projects/profile_pictures/', blank=True, null=True, validators=[validate_image_file_type, validate_image_file_size])
    banner_image = models.ImageField(upload_to='projects/banner_images/', blank=True, null=True, validators=[validate_image_file_type, validate_image_file_size])
    preferences = models.JSONField(default=get_default_preferences, blank=True)

    def set_preference(self, key, value):
        self.preferences[key] = value
        self.save()

    def get_preference(self, key, default=None):
        return self.preferences.get(key, default)

    def remove_preference(self, key):
        if key in self.preferences:
            del self.preferences[key]
            self.save()

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    MEMBER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]

    INVITE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=30)
    invite_status = models.CharField(max_length=10, choices=INVITE_STATUS_CHOICES, default='pending')
    # preferences = models.JSONField(default=get_default_preferences, blank=True)

    class Meta:
        unique_together = ('user', 'project')  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.get_invite_status_display()})"
