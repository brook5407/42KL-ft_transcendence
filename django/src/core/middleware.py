# core/middleware.py
from django.shortcuts import render
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class Custom404Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404 and not request.path.startswith('/api'):
            return render(request, 'index.html', status=404)
        return response
