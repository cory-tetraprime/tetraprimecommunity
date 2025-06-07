from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='received_messages'
    )
    subject = models.CharField(max_length=50, blank=True)
    body = models.TextField(max_length=500, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    # is_read = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies'
    )  # Reference to the parent message

    def mark_as_read(self):
        """Mark the message as read."""
        self.is_read = True
        self.save()


class MessageReadStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)


class Alert(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='alerts'
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    related_message = models.ForeignKey(
        'Message', on_delete=models.SET_NULL, blank=True, null=True, related_name='alerts'
    )
    alert_type = models.CharField(max_length=50, choices=[
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
    ])

    def mark_as_read(self):
        """Mark the alert as read."""
        self.is_read = True
        self.save()
