from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, EditProjectForm, AddMemberForm, EditMemberForm
from .models import Project, ProjectMembership
from django.contrib.auth import get_user_model
from django.contrib import messages

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

            if user:
                # Check if the user is already a member or invited
                if ProjectMembership.objects.filter(user=user, project=project).exists():
                    form.add_error('username', 'This user is already a member or has a pending invite.')
                else:
                    # Add the user as an invited member with 'pending' status
                    ProjectMembership.objects.create(
                        user=user,
                        project=project,
                        role='',
                        invite_status='pending'
                    )
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

