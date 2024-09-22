# core/middleware.py
from django.shortcuts import render
from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class Custom404Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404 and not request.path.startswith('/api'):
            return render(request, 'index.html', status=404)
        return response
    

class SetUserSettingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_language = request.user.profile.language
            snow_intensity = request.user.profile.snowIntensity
            translation.activate(user_language)
            request.LANGUAGE_CODE = user_language
            request.snow_intensity = snow_intensity

    def process_response(self, request, response):
        if request.user.is_authenticated and hasattr(request, 'snow_intensity'):
            snow_intensity = request.snow_intensity
            if snow_intensity:
                response.set_cookie('snow_intensity', snow_intensity, samesite='Lax')
        return response

