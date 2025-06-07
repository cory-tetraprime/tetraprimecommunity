from django import template

register = template.Library()


@register.filter
def get_preference(user, key):

    if hasattr(user, 'preferences') and isinstance(user.preferences, dict):
        return user.preferences.get(key)
    return None
