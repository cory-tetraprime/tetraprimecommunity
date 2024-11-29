from cProfile import label

from django import forms
from django.contrib.auth import get_user_model
from wagtail.users.forms import UserEditForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

User = get_user_model()


class CustomUserEditForm(UserEditForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label=_("Email"), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("First Name"), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("Last Name"), required=True)
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label=_("Country"))
    profile_picture = forms.ImageField(required=False)

    class Meta(UserEditForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'country', 'profile_picture']  # Add fields you want to edit
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)  # Don't save yet, to inspect data
        if self.cleaned_data.get('profile_picture'):
            uploaded_file = self.cleaned_data['profile_picture']
            print(f"File Name: {uploaded_file.name}")
            print(f"File Size: {uploaded_file.size} bytes")
        if commit:
            instance.save()
        return instance


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label=_("Email"), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("First Name"), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("Last Name"), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label=_("Country"))
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'country', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email exists for another user
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use by another user.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.set_password(self.cleaned_data["password1"])  # Hash the password
        if commit:
            user.save()
            if self.cleaned_data.get('profile_picture'):
                user.profile_picture = self.cleaned_data.get('profile_picture')
                user.save()  # Save the profile picture
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly remove unwanted fields
        for field_name in ['is_superuser', 'is_staff', 'groups', 'user_permissions']:
            if field_name in self.fields:
                del self.fields[field_name]
