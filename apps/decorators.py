from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            user = request.user

            
            if not user.is_authenticated:
                return redirect('/login/')

            
            user_role = getattr(user, 'role', None)

            
           
           
            if str(user_role) in allowed_roles:
                return view_func(request, *args, **kwargs)

           
            return redirect('/error/')

        return wrapper
    return decorator

