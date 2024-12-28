from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from projects.models import Project, ProjectMembership

User = get_user_model()


def discover_view(request):
    users = User.objects.filter(
        is_superuser=False
    ).filter(
        Q(preferences__private_profile=False) | Q(preferences__private_profile__isnull=True)
    ).exclude(
        id=request.user.id  # Exclude the current logged-in user
    ).order_by('-date_joined')

    paginator = Paginator(users, 10)  # Show 21 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    active_users_len = len(users)

    active_projects = Project.objects.filter(visibility='public').order_by('-updated_at')[:10]

    return render(request, 'social/discover.html', {'page_obj': page_obj, 'active_users_len': active_users_len, 'active_projects': active_projects})


def groups_view(request):
    return render(request, 'social/groups.html', {'user': request.user})


def tpc_whats_new(request):
    return render(request, 'social/whats-new.html', {'user': request.user})


def tpc_whats_new_release_notes(request):
    return render(request, 'social/release-notes.html', {'user': request.user})
