# import logging
# from wagtail import hooks
# from wagtail.users.views.users import UserCreationForm, UserEditForm
# from .forms import CustomUserCreationForm, CustomUserEditForm
#
# logger = logging.getLogger(__name__)
#
# logger.info("Loaded: wagtail_hooks.py")
#
#
# @hooks.register('register_user_creation_form')
# def use_custom_user_creation_form():
#     print("Custom User Creation Form Hook Executed")  # For debug purposes
#     logger.info("Custom User Creation Form Hook Executed")
#     return CustomUserCreationForm
#
#
# @hooks.register('register_user_edit_form')
# def use_custom_user_edit_form():
#     print("Custom User Edit Form Hook Executed")  # For debug purposes
#     logger.info("Custom User Edit Form Hook Executed")
#     return CustomUserEditForm
