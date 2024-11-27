from django import forms
from django.contrib.auth import get_user_model
from wagtail.users.forms import UserEditForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserEditForm(UserEditForm):
    country = forms.CharField(required=False, label=_("Country"))
    # profile_picture = forms.ImageField(required=False)

    class Meta(UserEditForm.Meta):
        model = User
        fields = UserEditForm.Meta.fields | {'country'}


class CustomUserCreationForm(UserCreationForm):
    country = forms.CharField(required=True, label=_("Country"))

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = UserCreationForm.Meta.fields | {'country'}
        fields = ['username', 'email', 'password1', 'password2', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly remove unwanted fields
        for field_name in ['is_superuser', 'is_staff', 'groups', 'user_permissions']:
            if field_name in self.fields:
                del self.fields[field_name]
