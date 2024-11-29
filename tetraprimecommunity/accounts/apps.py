from wagtail.users.apps import WagtailUsersAppConfig
from django.apps import AppConfig


class CustomUsersAppConfig(WagtailUsersAppConfig):
    user_viewset = "accounts.viewsets.UserViewSet"


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals