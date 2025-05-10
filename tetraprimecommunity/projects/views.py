# from lib2to3.fixes.fix_input import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, login_not_required
from .forms import ProjectForm, EditProjectForm, AddMemberForm, EditMemberForm, NextActionForm, EditProjectNoteForm, CreateProjectNoteForm
from .models import Project, ProjectMembership, NextAction, TeamMemberNote
from .services import Planner
from inbox.utils import create_alert, send_message_logic
from django.db.models import F, Subquery, OuterRef, Max
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import date

User = get_user_model()


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()

            # Add creator as manager
            ProjectMembership.objects.create(user=request.user, project=project, role='Project Creator', member_type='manager', invite_status='accepted')

            return redirect('my_projects')
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})


@login_required
def my_projects(request):
    # Get the user's project memberships
    pending_memberships = request.user.project_memberships.filter(invite_status='pending')
    active_memberships = request.user.project_memberships.filter(invite_status='accepted').exclude(project__creator=request.user)
    created_projects = request.user.created_projects.all()

    context = {
        'created_projects': created_projects,
        'pending_memberships': pending_memberships,
        'active_memberships': active_memberships,
    }
    return render(request, 'projects/my_projects.html', context)


@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)

    # Check if the profile is private
    if project.visibility == 'private' and request.user != project.creator:  # Default to False if preference doesn't exist
        # Render the private profile page
        return render(request, 'projects/private_project.html', {'profile_user': 'user'})

    members = ProjectMembership.objects.filter(project=project)
    active_memberships = project.memberships.filter(invite_status='accepted')

    # Check if the current user is an active member
    is_active_member = active_memberships.filter(user=request.user).exists()

    # Ensure the user has access to the project
    # if not (project.creator == request.user or members.filter(user=request.user).exists()):
    #     return redirect('my_projects')

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'active_memberships': active_memberships,
        'is_active_member': is_active_member,
    })


@login_required
def add_member(request, project_id):
    project = Project.objects.get(id=project_id)

    # Only allow the creator to invite members
    if project.creator != request.user:
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            role = form.cleaned_data['role']

            if user:
                # Check if the user is already a member or invited
                if ProjectMembership.objects.filter(user=user, project=project).exists():
                    form.add_error('username', 'This user is already a member or has a pending invite.')
                else:
                    # Add the user as an invited member with 'pending' status
                    ProjectMembership.objects.create(
                        user=user,
                        project=project,
                        role=role,
                        invite_status='pending'
                    )

                    # create_alert(
                    #     user=user,
                    #     title="New Project Invite",
                    #     body="Go to Your Projects to review.",
                    #     alert_type="info"
                    # )

                    # Get the invite message
                    invite_message = form.cleaned_data.get('invite_message', 'Greetings, you have been invited! Please review the Your Projects page. Thank you!')

                    sender = request.user
                    receiver_username = user.username
                    subject = f'Invite to: {project.name}'
                    body = invite_message

                    new_message, error = send_message_logic(sender, receiver_username, subject, body)

                    if error:
                        messages.error(request, f'Error: {error}', 'danger')
                    else:
                        messages.success(request, 'Project invite sent!', 'success')

                    return redirect('project_detail', project_id=project.id)
            else:
                form.add_error('username', 'User with this username does not exist.')
    else:
        form = AddMemberForm()

    return render(request, 'projects/add_member.html', {'form': form, 'project': project})


@login_required
def edit_member(request, membership_id):
    membership = get_object_or_404(ProjectMembership, id=membership_id)
    project = membership.project

    # Only allow project creator or managers to edit member roles
    if request.user != project.creator and not ProjectMembership.objects.filter(
            project=project, user=request.user, member_type='manager').exists():
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        form = EditMemberForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = EditMemberForm(instance=membership)

    return render(request, 'projects/edit_member.html', {'form': form, 'membership': membership, 'creator_id': project.creator_id})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure only the creator can edit the project
    print(project.creator)
    print(request.user)
    if project.creator != request.user:
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        form = EditProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = EditProjectForm(instance=project)

    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})


@login_required
def project_planner(request, project_id):
    # TODO: add action stage filtering, etc.

    # Define the mapping of action_stage to CSS classes
    stage_classes = {
        'progress': 'bg-success',
        'backlog': 'bg-info',
        'someday': 'bg-secondary',
        'review': 'bg-warning',
        'complete': 'bg-primary',
        'archived': 'bg-dark',
    }

    active_memberships = request.user.project_memberships.filter(invite_status='accepted').exclude(project__creator=request.user)  # Get the user's projects
    created_projects = request.user.created_projects.all()
    normalized_active_memberships = [
        membership.project for membership in active_memberships  # Normalize active_memberships to use the same structure as created_projects
    ]
    combined_projects = list(normalized_active_memberships) + list(created_projects)
    user_memberships = ProjectMembership.objects.filter(user=request.user)  # Get all project memberships for the user
    today = date.today()

    if project_id != 0:
        project = get_object_or_404(Project, id=project_id)
        planner = Planner(project)

        if request.method == 'POST' and 'add_action' in request.POST:
            # TODO: process form with Django forms
            title = request.POST.get('title')
            action_stage = request.POST.get('action_stage')
            due_date = request.POST.get('due_date')  # Fetch the field from POST data
            due_date = due_date if due_date else None  # Check if the field has a value; set to None if empty
            notes = request.POST.get('notes')

            try:
                assigned_to = ProjectMembership.objects.get(project=project, user=request.user)  # Get the membership for the current user and project
            except ProjectMembership.DoesNotExist:
                messages.error(request, 'You are not a member of this project.', 'danger')
                return redirect('project_planner', project_id=project_id)

            planner.create_action(title, action_stage, due_date, assigned_to, notes)

            messages.success(request, 'Next Action created successfully!', 'success')

        membership = ProjectMembership.objects.get(project=project, user=request.user)  # Get all project actions
        selected_stage = request.POST.get("action_stage", "progress")  # default if none selected
        project_actions = planner.get_member_actions(membership).filter(action_stage=selected_stage).order_by(F('due_date').asc(nulls_last=True), '-updated_at')

        for action in project_actions:
            action.is_due_today = action.due_date == today  # Add an 'is_due_today' flag to each action
            action.is_overdue = action.due_date and action.due_date < today  # Add an 'is_overdue' flag

        context = {'project': project, 'actions': project_actions, 'stage_classes': stage_classes, 'combined_projects': combined_projects, 'selected_stage': selected_stage, }

    else:
        selected_stage = request.POST.get("action_stage", "progress")  # default if none selected
        actions = NextAction.objects.filter(assigned_to__in=user_memberships, action_stage=selected_stage).order_by(F('due_date').asc(nulls_last=True), '-updated_at')  # Get all actions assigned to the user's memberships

        for action in actions:
            action.is_due_today = action.due_date == today  # Add an 'is_due_today' flag to each action
            action.is_overdue = action.due_date and action.due_date < today  # Add an 'is_overdue' flag

        context = {'combined_projects': combined_projects, 'actions': actions, 'stage_classes': stage_classes, 'selected_stage': selected_stage, }

    return render(request, 'projects/project_planner.html', context)


@login_required
def view_next_action(request, next_action_id):
    # Fetch the NextAction object or return 404 if not found
    next_action = get_object_or_404(NextAction, id=next_action_id)

    # Pass the project ID to the template
    project_id = next_action.project.id if next_action.project else None

    # Check if the current user has permission to edit (optional, if applicable)
    # For example, check if the user is the assigned_to or project owner
    if request.user != next_action.assigned_to.user:
        messages.error(request, "You don't have permission to edit this action.")
        return redirect('project_planner', project_id)  # Replace with your All Actions page URL

    # Handle POST request to update the action
    if request.method == 'POST':
        form = NextActionForm(request.POST, instance=next_action)
        if form.is_valid():
            form.save()
            messages.success(request, 'Next Action updated successfully!')
            return redirect('project_planner', project_id)  # Redirect back to the actions list
    else:
        # Prepopulate the form with the NextAction data
        form = NextActionForm(instance=next_action)

    return render(request, 'projects/view_next_action.html', {'form': form, 'next_action': next_action, 'project_id': project_id, })


@login_required
def project_notes(request, project_id):
    active_memberships = request.user.project_memberships.filter(invite_status='accepted').exclude(project__creator=request.user)  # Get the user's projects
    created_projects = request.user.created_projects.all()
    normalized_active_memberships = [
        membership.project for membership in active_memberships  # Normalize active_memberships to use the same structure as created_projects
    ]
    combined_projects = list(normalized_active_memberships) + list(created_projects)
    # user_memberships = ProjectMembership.objects.filter(user=request.user)  # Get all project memberships for the user

    if project_id != 0:
        project = get_object_or_404(Project, id=project_id)
        planner = Planner(project)
        membership = ProjectMembership.objects.get(project=project, user=request.user)
        notes = planner.get_member_notes(membership).order_by('-updated_at')
        # TODO: add notes pagination
        context = {'project': project, 'notes': notes, 'combined_projects': combined_projects, }

    else:
        # Subquery to get the latest updated_at timestamp for each project
        latest_notes = TeamMemberNote.objects.filter(
            project_membership__project=OuterRef('project_membership__project')
        ).order_by('-updated_at').values('id')[:1]

        # Main query to fetch only the most recent notes
        notes = TeamMemberNote.objects.filter(
            id__in=Subquery(latest_notes)
        ).order_by('-updated_at')
        context = {'combined_projects': combined_projects, 'notes': notes, }

    return render(request, 'projects/project_notes.html', context)  # TODO: optimize notes query


@login_required
def create_project_note(request, project_id):
    if request.method == 'POST':
        form = CreateProjectNoteForm(request.POST)
        if form.is_valid():
            project = get_object_or_404(Project, id=project_id)
            planner = Planner(project)
            membership = ProjectMembership.objects.get(project=project, user=request.user)
            # TODO: ensure user has permissions to create notes in the project (try/catch)

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            planner.add_member_note(membership, title, content)

            messages.success(request, 'Project note created successfully!', 'success')

            return redirect('project_notes', project_id)
    else:
        form = CreateProjectNoteForm()

    return render(request, 'projects/create_note.html', {'form': form})


@login_required
def view_project_note(request, note_id):
    project_note = get_object_or_404(TeamMemberNote, id=note_id)
    # Pass the project ID to the template
    project_id = project_note.project_membership.project.id if project_note.project_membership.project else None

    # Check if the current user has permission to edit (optional, if applicable)
    # For example, check if the user is the assigned_to or project owner
    if request.user != project_note.project_membership.user:
        messages.error(request, "You don't have permission to edit this action.")
        return redirect('project_notes', project_id)  # Replace with your All Actions page URL

    # Handle POST request to update the action
    if request.method == 'POST':
        form = EditProjectNoteForm(request.POST, instance=project_note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project note updated successfully!')
            return redirect('project_notes', project_id)  # Redirect back to the actions list
    else:
        # Prepopulate the form with the NextAction data
        form = EditProjectNoteForm(instance=project_note)

    return render(request, 'projects/view_note.html', {'form': form, 'project_note': project_note, 'project_id': project_id, })


def delete_note(request, note_id):
    # Retrieve the project (adjust as necessary for your setup)
    project = get_object_or_404(Project, id=request.POST.get('project_id'))
    project_note = get_object_or_404(TeamMemberNote, id=note_id)
    planner = Planner(project)

    if request.user != project_note.project_membership.user:
        messages.error(request, "You don't have permission delete note.")
        return redirect('project_notes', 0)

    if planner.delete_note(note_id):
        messages.success(request, "Note deleted successfully.")
    else:
        messages.error(request, "Note not found.")

    return redirect('project_notes', 0)


@login_required
def respond_to_invite(request, membership_id, action):
    try:
        # Fetch the membership and ensure it exists
        membership = ProjectMembership.objects.get(id=membership_id, invite_status='pending')
    except ProjectMembership.DoesNotExist:
        messages.error(request, 'Membership not found or already processed.', 'danger')
        return redirect('my_projects')

    # Check if the request is from the invitee
    if membership.user == request.user:
        if action == 'accept':
            membership.invite_status = 'accepted'
            membership.save()
            messages.success(request, 'You have accepted the invite!', 'success')
        elif action == 'decline':
            membership.invite_status = 'declined'
            membership.delete()
            messages.success(request, 'You have declined the invite.', 'success')
        else:
            messages.error(request, 'Invalid action for an invitee.', 'danger')
    # Check if the request is from the project creator
    elif membership.project.creator == request.user:
        if action == 'cancel':
            membership.invite_status = 'cancelled'
            membership.delete()
            messages.success(request, 'You have cancelled the invite.', 'success')
        else:
            messages.error(request, 'Invalid action for the project creator.', 'danger')
    else:
        # If neither the creator nor the invitee is making the request
        messages.error(request, 'You do not have permission to perform this action.', 'danger')

    return redirect('my_projects')

