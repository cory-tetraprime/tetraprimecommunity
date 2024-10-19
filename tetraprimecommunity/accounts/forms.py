from django import forms
from django.contrib.auth import get_user_model
from wagtail.users.forms import UserEditForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

# from .models import MembershipStatus

User = get_user_model()


class CustomUserEditForm(UserEditForm):
    country = forms.CharField(required=False, label=_("Country"))
    # status = forms.ModelChoiceField(queryset=MembershipStatus.object, required=True, label=_("Membership Status"))

    class Meta(UserEditForm.Meta):
        model = User
        fields = UserEditForm.Meta.fields | {'country'}


class CustomUserCreationForm(UserCreationForm):
    country = forms.CharField(required=False, label=_("Country"))
    # status = forms.ModelChoiceField(queryset=MembershipStatus.object, required=False, label=_("Membership Status"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields | {'country'}
