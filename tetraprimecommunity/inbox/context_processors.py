from inbox.views import get_unread_counts


def unread_counts_processor(request):
    if request.user.is_authenticated:
        return {'unread_counts': get_unread_counts(request.user)}
    return {'unread_counts': None}
