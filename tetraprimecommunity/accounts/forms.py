from cProfile import label

from django import forms
from django.contrib.auth import get_user_model
from wagtail.users.forms import UserEditForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

User = get_user_model()


class CustomUserEditForm(UserEditForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'rows': 3}), label=_("Email"), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 3}), label=_("First Name"), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 3}), label=_("Last Name"), required=True)
    COUNTRY_CHOICES = [
        ('', 'Select your country'),  # Default blank option
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('00', 'Other'),
    ]
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label=_("Country")
    )
    # country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 3}), required=True, label=_("Country"))
    profile_picture = forms.ImageField(required=False)
    banner_image = forms.ImageField(required=False)
    bio_intro = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label=_("Bio Intro"), max_length=500, required=False)
    bio_current_professional_title = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Current Professional Title"), max_length=500, required=False)
    bio_top_technical_skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Top Technical Skills"), max_length=500, required=False)
    bio_relevant_certifications = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Relevant Certifications"), max_length=500, required=False)
    bio_favorite_tools_and_technologies = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Favorite Tools & Technologies"), max_length=500, required=False)
    bio_career_goals = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Career Goals"), max_length=500, required=False)
    bio_dream_project = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Dream Project"), max_length=500, required=False)
    bio_projects_youre_proud_of = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Projects You're Proud Of"), max_length=500, required=False)
    bio_areas_for_growth = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Areas for Growth"), max_length=500, required=False)
    bio_open_for_collaboration_on = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Open for Collaboration On"), max_length=500, required=False)
    bio_seeking_a_mentor = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Seeking a Mentor"), max_length=500, required=False)
    bio_open_to_mentoring_others = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Open to Mentoring Others"), max_length=500, required=False)
    bio_need_help_with = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Need Help With"), max_length=500, required=False)
    bio_favorite_quote = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Favorite Quote"), max_length=500, required=False)
    bio_superpower = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Superpower"), max_length=500, required=False)
    bio_first_experience_in_tech = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("First Experience in Tech"), max_length=500, required=False)
    bio_hobbies_and_passions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label=_("Hobbies & Passions"), max_length=500, required=False)

    class Meta(UserEditForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'country', 'profile_picture', 'banner_image']  # Add fields you want to edit
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill the form with existing bio_intro from preferences
        instance = kwargs.get('instance')
        if instance:
            self.fields['bio_intro'].initial = instance.preferences.get('bio_intro', '')
            self.fields['bio_current_professional_title'].initial = instance.preferences.get('bio_current_professional_title', '')
            self.fields['bio_top_technical_skills'].initial = instance.preferences.get('bio_top_technical_skills', '')
            self.fields['bio_relevant_certifications'].initial = instance.preferences.get('bio_relevant_certifications', '')
            self.fields['bio_favorite_tools_and_technologies'].initial = instance.preferences.get('bio_favorite_tools_and_technologies', '')
            self.fields['bio_career_goals'].initial = instance.preferences.get('bio_career_goals', '')
            self.fields['bio_dream_project'].initial = instance.preferences.get('bio_dream_project', '')
            self.fields['bio_projects_youre_proud_of'].initial = instance.preferences.get('bio_projects_youre_proud_of', '')
            self.fields['bio_areas_for_growth'].initial = instance.preferences.get('bio_areas_for_growth', '')
            self.fields['bio_open_for_collaboration_on'].initial = instance.preferences.get('bio_open_for_collaboration_on', '')
            self.fields['bio_seeking_a_mentor'].initial = instance.preferences.get('bio_seeking_a_mentor', '')
            self.fields['bio_open_to_mentoring_others'].initial = instance.preferences.get('bio_open_to_mentoring_others', '')
            self.fields['bio_need_help_with'].initial = instance.preferences.get('bio_need_help_with', '')
            self.fields['bio_favorite_quote'].initial = instance.preferences.get('bio_favorite_quote', '')
            self.fields['bio_superpower'].initial = instance.preferences.get('bio_superpower', '')
            self.fields['bio_first_experience_in_tech'].initial = instance.preferences.get('bio_first_experience_in_tech', '')
            self.fields['bio_hobbies_and_passions'].initial = instance.preferences.get('bio_hobbies_and_passions', '')

    def save(self, commit=True):
        instance = super().save(commit=False)  # Don't save yet, to inspect data

        # if self.cleaned_data.get('profile_picture'):
        #     uploaded_file = self.cleaned_data['profile_picture']

        # if self.cleaned_data.get('banner_image'):
        #     uploaded_file = self.cleaned_data['banner_image']

        if self.cleaned_data.get('bio_intro'):
            # if form.is_valid():
            preferences = instance.preferences or {}  # Ensure it's a dictionary
            for field_name, value in self.cleaned_data.items():
                if field_name.startswith('bio_') and value is not None:  # Check for 'bio_' prefix and non-empty values
                    preferences[field_name] = value.strip() if isinstance(value, str) else value  # Handle strings
            instance.preferences = preferences  # Reassign explicitly

        if commit:
            instance.save()
        return instance


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=40, widget=forms.EmailInput(attrs={'class': 'form-control'}), label=_("Email"), required=True)
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("First Name"), required=True)
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_("Last Name"), required=True)
    password1 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
    password2 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")
    COUNTRY_CHOICES = [
        ('', 'Select your country'),  # Default blank option
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('00', 'Other'),
    ]
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label=_("Country"),
        initial='US'
    )
    # country = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label=_("Country"))
    invite_code = forms.CharField(max_length=100, required=True, help_text="Enter your invite code.", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'country']
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

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        correct_code = "Q7b!JSCCxqdvV%fV7L7oGi@6AAzsiE4F9R8FZBab"  # Replace with your hardcoded invite code

        if invite_code != correct_code:
            raise forms.ValidationError("Invalid invite code. Please try again.")

        return invite_code

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
