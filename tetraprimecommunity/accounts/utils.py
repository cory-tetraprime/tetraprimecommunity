def get_user_timezone(request):
    """
    Retrieve the user's timezone or return UTC as the default.
    """
    if request.user.is_authenticated:
        # Return the user's timezone if set, otherwise fall back to UTC
        return getattr(request.user, 'timezone', 'UTC') or 'UTC'
    return 'UTC'
