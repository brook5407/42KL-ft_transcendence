from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from allauth.account.models import EmailAddress
from django.core.exceptions import ObjectDoesNotExist
from core import settings
from utils.request_helpers import is_ajax_request
from django.views.decorators.http import require_POST

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
def forget_password_modal(request):
    if is_ajax_request(request):
        return render(request, 'components/modals/forget-password.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")


@api_view(['GET'])
def reset_password_modal(request):
    if is_ajax_request(request):
        return render(request, 'components/modals/reset-password.html')
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
    try:
        email_verified = EmailAddress.objects.get(user=user, primary=True) is not None
    except ObjectDoesNotExist:
        email_verified = False
    
    profile = user.profile
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email_verified': email_verified,
        'profile': {
            'bio': profile.bio,
            'avatar': profile.avatar.url,
            'nickname': profile.nickname,
        }
    }
    return JsonResponse(data)

@require_POST
@csrf_exempt
def custom_set_language(request):
    next_url = request.POST.get('next', request.GET.get('next'))
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = request.META.get('HTTP_REFERER', '/')
        if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = '/'

    language = request.POST.get('language', settings.LANGUAGE_CODE)
    if language and language in [lang[0] for lang in settings.LANGUAGES]:
        activate(language)
        request.session[settings.LANGUAGE_CODE] = language

        # Update user's profile language
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                profile.language = language
                profile.save()
            except request.user.profile.RelatedObjectDoesNotExist:
                # Handle case where user doesn't have a profile
                pass
            
    response = HttpResponseRedirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return HttpResponseRedirect(next_url)

