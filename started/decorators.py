from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import Owner, Client

def owner_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.user.owner
            return view_func(request, *args, **kwargs)
        except Owner.DoesNotExist:
            messages.error(request, 'Access denied. Owner account required.')
            return redirect('login')
    return _wrapped_view

def client_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.user.client
            return view_func(request, *args, **kwargs)
        except Client.DoesNotExist:
            messages.error(request, 'Access denied. Client account required.')
            return redirect('login')
    return _wrapped_view