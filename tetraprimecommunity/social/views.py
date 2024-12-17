from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

User = get_user_model()


def people_view(request):
    users = User.objects.filter(
        is_superuser=False
    ).filter(
        Q(preferences__private_profile=False) | Q(preferences__private_profile__isnull=True)
    ).exclude(
        id=request.user.id  # Exclude the current logged-in user
    ).order_by('date_joined')

    paginator = Paginator(users, 21)  # Show 21 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'social/people.html', {'page_obj': page_obj})


def groups_view(request):
    return render(request, 'social/groups.html', {'user': request.user})
