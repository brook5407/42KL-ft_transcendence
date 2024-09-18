from django.http import HttpRequest
from functools import wraps
from django.shortcuts import render, redirect
import requests
from django.conf import settings


def is_ajax_request(request: HttpRequest):
	return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def authenticated_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        
        # User is authenticated, proceed with the view
        return view_func(request, *args, **kwargs)
    return wrapper