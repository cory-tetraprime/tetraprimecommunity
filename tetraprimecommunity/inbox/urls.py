from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.read_message, name='read_message'),
    path('alert/<int:alert_id>/', views.read_alert, name='read_alert'),
    path('send_message/', views.send_message, name='send_message'),
    path('thread/<int:thread_id>/', views.view_thread, name='view_thread'),  # Threaded view
    path('thread/delete/<int:message_id>/', views.delete_message_thread, name='delete_message_thread'),
    path('send_alert/', views.send_alert, name='send_alert'),
    path('alert/delete/<int:alert_id>/', views.delete_alert, name='delete_alert'),
]
