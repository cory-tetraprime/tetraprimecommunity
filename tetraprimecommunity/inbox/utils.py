from django.utils.timezone import now
from .models import Alert, CustomUser
from .models import Message, MessageReadStatus, CustomUser


def send_message_logic(sender, receiver_username, subject, body):
    """
    Handles the logic for sending a message.
    """
    try:
        receiver = CustomUser.objects.get(username=receiver_username)
        new_message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            subject=subject,
            body=body
        )
        # Create initial read statuses
        MessageReadStatus.objects.create(message=new_message, user=new_message.sender, is_read=True, read_at=now())  # Sender has already read it
        MessageReadStatus.objects.create(message=new_message, user=new_message.receiver, is_read=False)  # Receiver hasn't read it yet

        return new_message, None  # No errors
    except CustomUser.DoesNotExist:
        return None, "Receiver not found."


def create_alert(user, title, body='', alert_type='info', related_message=None):
    if not isinstance(user, CustomUser):
        raise ValueError("The 'user' parameter must be an instance of CustomUser.")

    alert = Alert.objects.create(
        user=user,
        title=title,
        body=body,
        created_at=now(),
        is_read=False,
        alert_type=alert_type,
        related_message=related_message,
    )
    return alert
