from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserEditForm

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserEditForm
    model = CustomUser
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login']

    # To display custom fields in the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Custom User Info', {'fields': ('country', 'profile_picture', 'preferences')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom User Info', {'fields': ('country', 'profile_picture', 'preferences')}),
    )


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
#
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {"fields": ("country", "profile_picture", "preferences")}),
#     )
#     list_display = ["username", "email", "country", "is_staff"]
#
# admin.site.register(CustomUser, CustomUserAdmin)
