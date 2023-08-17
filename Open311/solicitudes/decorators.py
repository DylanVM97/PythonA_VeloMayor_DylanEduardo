from django.shortcuts import redirect
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# Revisa si el usuario tiene el grupo requerido
def user_has_group(group_names):

    list = [word.strip() for word in group_names.split(',')]
    
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name__in=list).exists() or request.user.is_superuser or request.user.is_staff:
                    return view_func(request, *args, **kwargs)
                elif request.user.groups.filter(name='servidor').exists():
                    messages.warning(request, 'No tienes permisos o grupos asignados para entrar a esta zona')
                    return redirect('servidor')
                elif request.user.groups.filter(name='ciudadano').exists():
                    messages.warning(request, 'No tienes permisos o grupos asignados para entrar a esta zona')
                    return redirect('productos')
            else:
                return redirect('login')
        return _wrapped_view
    return decorator
