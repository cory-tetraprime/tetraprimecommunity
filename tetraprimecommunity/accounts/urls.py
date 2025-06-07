from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from .views import signup_view, profile_view, profile_view_user, edit_profile_view, change_password_view, UserPreferencesView, username_search

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('profile/', profile_view, name='profile'),
    path('profile/@<str:username>', profile_view_user, name='profile_user'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('change-password/', change_password_view, name='change_password'),
    path('preferences/', UserPreferencesView.as_view(), name='user_preferences'),
    path('username-search/', username_search, name='username_search'),
]
