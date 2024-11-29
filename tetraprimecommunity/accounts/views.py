from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


def signup_view(request):
    # Redirect logged-in users to their profile
    if request.user.is_authenticated:
        return redirect('profile')  # Replace 'profile' with the name of your profile URL pattern

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful sign-up
            # login(request, user)
            return redirect('login')  # Redirect to the home page or a success page
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print('Form is valid!')
            user = form.save()
            print(f"Uploaded file URL: {user.profile_picture.url}")
            print(f"Uploaded file path: {user.profile_picture.path}")
            return redirect('profile')  # Redirect to profile page after saving
        else:
            print('Form is invalid!')
            print(form.errors)
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to the profile page or another page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


class CustomLogoutView(LogoutView):
    # Add any custom logic here, such as logging or extra messages
    pass
