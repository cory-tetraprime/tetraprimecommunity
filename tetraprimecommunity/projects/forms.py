from django import forms
from .models import Project, ProjectMembership, NextAction, TeamMemberNote


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'visibility']
        labels = {
            'name': 'Project Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
        }


class AddMemberForm(forms.Form):
    username = forms.CharField(label="Invite Member by Username", required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    role = forms.CharField(label="Team Member Role", required=True, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))

    invite_message = forms.CharField(
        required=False,  # Allow this field to be optional
        widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Please add an invite message...'})
    )


class EditMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ['member_type', 'role']  # Add other fields if needed
        labels = {
            'member_type': 'Member Type',
            'role': 'Role',
        }
        widgets = {
            'member_type': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'visibility', 'profile_picture', 'banner_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class NextActionForm(forms.ModelForm):
    class Meta:
        model = NextAction
        fields = ['title', 'action_stage', 'due_date', 'notes']  # Include editable fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'action_stage': forms.Select(attrs={'class': 'form-control mb-3'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }


class CreateProjectNoteForm(forms.ModelForm):
    class Meta:
        model = TeamMemberNote
        fields = ['title', 'content']  # Include editable fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'content': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }


class EditProjectNoteForm(forms.ModelForm):
    class Meta:
        model = TeamMemberNote
        fields = ['title', 'content']  # Include editable fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3 fs-5'}),
            'content': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': '20', }),
        }
