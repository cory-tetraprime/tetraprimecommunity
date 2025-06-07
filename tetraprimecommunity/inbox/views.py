from .forms import WriteNewMessageForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, Value, Q, Subquery, OuterRef, Exists
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from inbox.models import Message, Alert, MessageReadStatus
from inbox.utils import create_alert, send_message_logic
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import models
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.conf import settings

CustomUser = get_user_model()


@login_required
def inbox(request, user_name=None):
    # Initialize both forms
    message_form = WriteNewMessageForm(prefix='message')
    message_to = user_name or ""

    # Fetch latest messages by thread for received messages
    received_messages = (
        Message.objects.filter(receiver=request.user, parent__isnull=True)
        .annotate(thread_id=Coalesce('parent_id', 'id'))
        .annotate(
            latest_message_time=Subquery(  # Get the latest sent_at time for the thread
                Message.objects.filter(
                    models.Q(parent=OuterRef('id')) | models.Q(id=OuterRef('id'))  # Parent or itself
                ).order_by('-sent_at').values('sent_at')[:1]
            )
        )
        .annotate(
            latest_message_body=Subquery(  # Get the latest sent_at time for the thread
                Message.objects.filter(
                    models.Q(parent=OuterRef('id')) | models.Q(id=OuterRef('id'))  # Parent or itself
                ).order_by('-sent_at').values('body')[:1]
            )
        )
        .annotate(item_type=Value('message', output_field=models.CharField()))
        .annotate(
            has_unread=Exists(  # Check if there are unread messages in the thread
                MessageReadStatus.objects.filter(
                    models.Q(message__parent=OuterRef('id')) | models.Q(message__id=OuterRef('id')),
                    user=request.user,
                    is_read=False
                )
            )
        )
        .select_related('sender', 'receiver')  # Optimize by fetching related user details
        .values(
            'id', 'subject', 'sent_at', 'item_type', 'sender_id', 'receiver_id', 'sender__profile_picture', 'sender__username', 'receiver__profile_picture', 'receiver__username', 'thread_id', 'has_unread', 'latest_message_time', 'latest_message_body'
        )
    )

    # Fetch latest messages by thread for sent messages
    sent_messages = (
        Message.objects.filter(sender=request.user, parent__isnull=True)
        .annotate(thread_id=Coalesce('parent_id', 'id'))
        .annotate(
            latest_message_time=Subquery(  # Get the latest sent_at time for the thread
                Message.objects.filter(
                    models.Q(parent=OuterRef('id')) | models.Q(id=OuterRef('id'))  # Parent or itself
                ).order_by('-sent_at').values('sent_at')[:1]
            )
        )
        .annotate(
            latest_message_body=Subquery(  # Get the latest sent_at time for the thread
                Message.objects.filter(
                    models.Q(parent=OuterRef('id')) | models.Q(id=OuterRef('id'))  # Parent or itself
                ).order_by('-sent_at').values('body')[:1]
            )
        )
        .annotate(item_type=Value('message', output_field=models.CharField()))
        .annotate(
            has_unread=Exists(  # Check if there are unread messages in the thread
                MessageReadStatus.objects.filter(
                    models.Q(message__parent=OuterRef('id')) | models.Q(message__id=OuterRef('id')),
                    user=request.user,
                    is_read=False
                )
            )
        )
        .select_related('sender', 'receiver')  # Optimize by fetching related user details
        .values(
            'id', 'subject', 'sent_at', 'item_type', 'sender_id', 'receiver_id', 'receiver__profile_picture', 'receiver__username', 'sender__profile_picture', 'sender__username', 'thread_id', 'has_unread', 'latest_message_time', 'latest_message_body'
        )
    )

    # Combine received and sent messages
    combined_messages = list(received_messages) + list(sent_messages)

    # Add profile picture paths dynamically based on the other person in the conversation
    for message in combined_messages:
        if message['sender_id'] == message['receiver_id']:  # Self-sent message
            other_user_profile_picture = message['sender__profile_picture']
            other_user_username = message['sender__username']
        elif message['sender_id'] == request.user.id:  # If the logged-in user is the sender
            other_user_profile_picture = message['receiver__profile_picture']
            other_user_username = message['receiver__username']
        else:  # If the logged-in user is the receiver
            other_user_profile_picture = message['sender__profile_picture']
            other_user_username = message['sender__username']

        # Update the message with the other user's profile picture and username
        message['other_user_profile_picture'] = (
            request.build_absolute_uri(f"{settings.MEDIA_URL}{other_user_profile_picture}")
            if other_user_profile_picture
            else request.build_absolute_uri(f"{settings.STATIC_URL}custom/images/user-pfp-generic.png")
        )
        message['other_user_username'] = other_user_username

    # Sort messages by latest_message_time in descending order
    sorted_messages = sorted(combined_messages, key=lambda x: x['latest_message_time'], reverse=True)

    # Fetch alerts (unchanged)
    alerts = (
        Alert.objects.filter(user=request.user)
        .annotate(
            item_type=Value('alert', output_field=models.CharField()),
            sent_at=Coalesce('created_at', 'created_at'),  # Ensure sorting compatibility
        )
        .values('id', 'title', 'body', 'is_read', 'sent_at', 'item_type', 'related_message')
    )

    # Add default 'latest_message_time' to alerts for consistent sorting
    for alert in alerts:
        alert['latest_message_time'] = alert['sent_at']  # Use 'sent_at' for sorting alerts

    # Combine messages and alerts
    combined_items = sorted(list(sorted_messages) + list(alerts), key=lambda x: x['latest_message_time'], reverse=True)

    # Sort combined items by latest_message_time
    sorted_items = sorted(combined_items, key=lambda x: x.get('latest_message_time', None), reverse=True)

    return render(request, 'inbox/inbox.html', {'items': sorted_items, 'message_form': message_form, 'message_to': message_to})


@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver_username')  # Fetch username instead of ID
        # subject = request.POST.get('subject', '')
        subject = ''
        body = request.POST.get('body')

        # Use the utility function
        new_message, error = send_message_logic(request.user, receiver_username, subject, body)

        if error:
            messages.error(request, error, 'danger')
        else:
            messages.success(request, 'Message sent successfully!', 'success')

    return redirect('inbox')


@login_required
def reply_message(request, original_message_id):
    try:
        # Fetch the original message to reply to
        original_message = Message.objects.get(id=original_message_id, receiver=request.user)

        if request.method == 'POST':
            body = request.POST.get('body')
            subject = f"Re: {original_message.subject}"
            receiver = original_message.sender

            # Create the reply and associate it with the thread
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                subject=subject,
                body=body,
                parent=original_message,  # Associate reply with the original message
            )
            messages.success(request, 'Reply sent successfully!')
            return redirect('inbox')

        # Render reply form with prefilled data
        return render(request, 'reply_message.html', {
            'original_message': original_message,
            'receiver_username': original_message.sender.username,
        })

    except Message.DoesNotExist:
        messages.error(request, 'Message not found.')
        return redirect('inbox')


@login_required
def view_thread(request, thread_id):
    try:
        # Fetch the parent message and its replies
        thread_messages = Message.objects.filter(
            models.Q(id=thread_id) | models.Q(parent_id=thread_id)
        ).order_by('sent_at')

        parent_message = thread_messages.first()  # Get the parent message

        # Mark unread messages as read for the current user
        unread_statuses = MessageReadStatus.objects.filter(
            message__in=thread_messages, user=request.user, is_read=False
        )
        unread_statuses.update(is_read=True, read_at=now())

        if request.method == 'POST':
            # Handle reply submission
            body = request.POST.get('body')
            if body.strip():  # Ensure the reply is not empty
                new_message = Message.objects.create(
                    sender=request.user,
                    receiver=parent_message.sender if parent_message.receiver == request.user else parent_message.receiver,
                    subject={parent_message.subject},
                    body=body,
                    parent=parent_message,
                )
                # Create initial read status for the new message
                MessageReadStatus.objects.create(message=new_message, user=new_message.sender, is_read=True, read_at=now())
                MessageReadStatus.objects.create(message=new_message, user=new_message.receiver, is_read=False)

                messages.success(request, 'Reply sent successfully!')
                return redirect('view_thread', thread_id=parent_message.id)

        return render(request, 'inbox/thread_view.html', {
            'thread_messages': thread_messages,
            'parent_message': parent_message,
        })

    except Message.DoesNotExist:
        messages.error(request, 'Thread not found.')
        return redirect('inbox')


@login_required
def read_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, receiver=request.user)
        message.mark_as_read()
        return render(request, 'inbox/message_detail.html', {'message': message})
    except Message.DoesNotExist:
        messages.error(request, 'Message not found.')
        return redirect('inbox')


@login_required
def delete_message_thread(request, message_id):
    # Fetch the message
    message = get_object_or_404(Message, id=message_id)

    # Ensure the user is authorized to delete the thread
    if request.user != message.sender and request.user != message.receiver:
        return HttpResponseForbidden("You are not authorized to delete this thread.")

    # Delete the thread: parent message and all replies
    if message.parent is None:  # It's a parent message
        Message.objects.filter(Q(id=message.id) | Q(parent=message)).delete()
    else:  # It's a reply, so delete its thread
        Message.objects.filter(Q(id=message.parent.id) | Q(parent=message.parent)).delete()

    messages.success(request, "Thread deleted successfully.")
    return redirect('inbox')


@login_required
def mark_message_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id, receiver=request.user)
        message.mark_as_read()
        messages.success(request, 'Message marked as read.')
    except Message.DoesNotExist:
        messages.error(request, 'Message not found.')

    return redirect('inbox')


@login_required
def read_alert(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id, user=request.user)
        alert.mark_as_read()
        return render(request, 'inbox/alert_detail.html', {'alert': alert})
    except Alert.DoesNotExist:
        messages.error(request, 'Alert not found.')
        return redirect('inbox')


# def create_alert(user, title, body='', alert_type='info', related_message=None):
#     if not isinstance(user, CustomUser):
#         raise ValueError("The 'user' parameter must be an instance of CustomUser.")
#
#     alert = Alert.objects.create(
#         user=user,
#         title=title,
#         body=body,
#         created_at=now(),
#         is_read=False,
#         alert_type=alert_type,
#         related_message=related_message,
#     )
#     return alert


@login_required
def delete_alert(request, alert_id):
    # Fetch the alert
    alert = get_object_or_404(Alert, id=alert_id)

    # Ensure the logged-in user is the owner of the alert
    if request.user != alert.user:
        return HttpResponseForbidden("You are not authorized to delete this alert.")

    # Delete the alert
    alert.delete()
    messages.success(request, "Alert deleted successfully.")
    return redirect('inbox')


@login_required
def send_alert(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver_username')
        title = request.POST.get('title', 'New Alert')
        body = request.POST.get('body', '')
        alert_type = request.POST.get('alert_type', 'info')

        try:
            # Fetch the recipient by username
            receiver = CustomUser.objects.get(username=receiver_username)

            # Create the alert
            create_alert(
                user=receiver,
                title=title,
                body=body,
                alert_type=alert_type
            )

            messages.success(request, 'Alert sent successfully!', 'success')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Receiver not found.', 'danger')

    return redirect('inbox')


def get_unread_counts(user):
    unread_message_count = MessageReadStatus.objects.filter(user=user, is_read=False).count()
    unread_alert_count = Alert.objects.filter(user=user, is_read=False).count()
    unread_total = unread_message_count + unread_alert_count
    return {
        'unread_messages': unread_message_count,
        'unread_alerts': unread_alert_count,
        'unread_total': unread_total,
    }
