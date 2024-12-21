from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


User = get_user_model()


def signup_view(request):
    # Redirect logged-in users to their profile
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'You may now sign-in!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    # Logged in user profile view
    user = request.user
    profile_status = user.profile_completion_status()  # Retrieve completion status
    return render(
        request,
        'accounts/profile.html',
        {'user': user, 'profile_status': profile_status, 'profile_user': request.user}  # Pass status to template
    )


@login_required
def profile_view_user(request, username):
    if request.user.username == username:
        return redirect('profile')

    # Fetch the user object using the username
    user = get_object_or_404(User, username=username)

    # Check if the profile is private
    if user.get_preference('private_profile', False):  # Default to False if preference doesn't exist
        # Render the private profile page
        return render(request, 'accounts/private_profile.html', {'profile_user': user})

    # Pass the user to your template or handle your logic
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)  # Save instance without committing yet
            preferences = user.preferences  # Update preferences from POST data

            preferences['bio_intro'] = request.POST.get('bio_intro', '').strip()
            preferences['bio_current_professional_title'] = request.POST.get('bio_current_professional_title', '').strip()
            preferences['bio_top_technical_skills'] = request.POST.get('bio_top_technical_skills', '').strip()
            preferences['bio_relevant_certifications'] = request.POST.get('bio_relevant_certifications', '').strip()
            preferences['bio_favorite_tools_and_technologies'] = request.POST.get('bio_favorite_tools_and_technologies', '').strip()
            preferences['bio_career_goals'] = request.POST.get('bio_career_goals', '').strip()
            preferences['bio_dream_project'] = request.POST.get('bio_dream_project', '').strip()
            preferences['bio_projects_youre_proud_of'] = request.POST.get('bio_projects_youre_proud_of', '').strip()
            preferences['bio_areas_for_growth'] = request.POST.get('bio_areas_for_growth', '').strip()
            preferences['bio_open_for_collaboration_on'] = request.POST.get('bio_open_for_collaboration_on', '').strip()
            preferences['bio_seeking_a_mentor'] = request.POST.get('bio_seeking_a_mentor', '').strip()
            preferences['bio_open_to_mentoring_others'] = request.POST.get('bio_open_to_mentoring_others', '').strip()
            preferences['bio_need_help_with'] = request.POST.get('bio_need_help_with', '').strip()
            preferences['bio_favorite_quote'] = request.POST.get('bio_favorite_quote', '').strip()
            preferences['bio_superpower'] = request.POST.get('bio_superpower', '').strip()
            preferences['bio_first_experience_in_tech'] = request.POST.get('bio_first_experience_in_tech', '').strip()
            preferences['bio_hobbies_and_passions'] = request.POST.get('bio_hobbies_and_passions', '').strip()

            preferences['private_profile'] = request.POST.get('private_profile') == 'on'
            preferences['dark_mode'] = request.POST.get('dark_mode') == 'on'
            preferences['email_notifications'] = request.POST.get('email_notifications') == 'on'
            preferences['language'] = request.POST.get('language', 'en')
            preferences['onboarding'] = request.POST.get('onboarding') == 'on'

            user.save()  # Save the user first to ensure the file is saved to its final destination
            user.preferences = preferences
            user.save()
            messages.success(request, 'Your profile has been saved.', 'success')
            return redirect('edit_profile')  # Redirect to profile page after saving
        else:
            # Reload the user instance to discard invalid file uploads
            with transaction.atomic():
                request.user.refresh_from_db()
            print(form.errors)
            messages.error(request, 'Error saving your profile.', 'danger')
            print("Profile picture in database:", request.user.profile_picture)

            return render(request, 'accounts/edit_profile.html', {'form': form, 'profile_user': request.user})  # Redirect to profile page with error message
    else:
        form = CustomUserEditForm(instance=request.user)

    context = {
        'form': form,
        'preferences': request.user.preferences,  # Add preferences to context
        'profile_user': request.user
    }
    return render(request, 'accounts/edit_profile.html', context)


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


@login_required
def profile_checklist(request):
    user = request.user
    status = user.profile_completion_status()
    return render(request, 'templates/accounts/includes/onboard-new-user.html', {'status': status, 'user': user})


class UserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(request.user.preferences)

    def post(self, request):
        for key, value in request.data.items():
            request.user.set_preference(key, value)
        return Response(request.user.preferences)
