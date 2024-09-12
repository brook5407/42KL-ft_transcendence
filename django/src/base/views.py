from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from allauth.account.models import EmailAddress
from core import settings
from utils.request_helpers import is_ajax_request


User = get_user_model()

@api_view(['GET'])
def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def home(request):
    if is_ajax_request(request):
        return render(request, 'components/pages/home.html')
    return render(request, 'index.html')

@api_view(['GET'])
def signin_modal(request):
    if is_ajax_request(request):
        context = {
            'otp_auth': settings.OTP_AUTH,
        }
        return render(request, 'components/modals/signin.html', context=context)
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
def signup_modal(request):
    if is_ajax_request(request):
        return render(request, 'components/modals/signup.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
def oauth42_modal(request):
    if is_ajax_request(request):
        return render(request, 'components/modals/42oauth.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def settings_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/settings.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_profile(request):
    user = request.user
    profile = user.profile
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email_verified': True if EmailAddress.objects.get(user=user, primary=True) else False,
        'profile': {
            'bio': profile.bio,
            'avatar': profile.avatar.url,
            'nickname': profile.nickname,
        }
    }
    return JsonResponse(data)
