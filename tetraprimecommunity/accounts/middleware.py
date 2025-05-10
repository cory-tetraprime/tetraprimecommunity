from django.utils.timezone import activate, deactivate
from .utils import get_user_timezone  # Import your utility function


class CustomTimezoneMiddleware:
    """
    Custom middleware to activate the user's timezone for each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine the timezone dynamically
        timezone = get_user_timezone(request)
        if timezone:
            activate(timezone)
        else:
            deactivate()

        # Process the response
        response = self.get_response(request)

        # Deactivate timezone after the request is processed
        deactivate()

        return response
