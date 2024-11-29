from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

User = get_user_model()


def people_view(request):
    users = User.objects.filter(is_superuser=False).order_by('username')
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'social/people.html', {'page_obj': page_obj})
