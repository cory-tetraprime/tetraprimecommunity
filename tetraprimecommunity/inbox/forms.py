from django import forms
from .models import Message


class WriteNewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'body']
        labels = {'receiver': 'Send to', 'body': 'Message', }
        widgets = {
            'receiver': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


# class SendNewAlertForm(forms.ModelForm):
#     class Meta:
#         model = Alert
#         fields = ['user', 'title', 'body', 'alert_type']
#         labels = {'user': 'Send to', 'title': 'Alert Title', 'body': 'Alert Message', 'alert_type': 'Alert Type', }  # alert_type
#         widgets = {
#             'user': forms.TextInput(attrs={'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control'}),
#             'alert_type': forms.Select(attrs={'class': 'form-control'}),
#         }
