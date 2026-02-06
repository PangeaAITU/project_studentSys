from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            user_role = request.user.profile.role

            if user_role not in allowed_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


def exclude_role(excluded_roles=[]):
    """Decorator to deny access to specific roles."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            user_role = request.user.profile.role

            if user_role in excluded_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

