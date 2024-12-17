from django.templatetags.static import static


def global_variables(request):
    return {
        'GENERIC_USER_PFP': static('custom/images/user-pfp-generic.png')
    }
