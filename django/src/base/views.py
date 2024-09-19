from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from allauth.account.models import EmailAddress
from django.core.exceptions import ObjectDoesNotExist
from core import settings
from utils.request_helpers import is_ajax_request, authenticated_view
from pong.models import UserActiveTournament
from django.views.decorators.http import require_GET, require_POST
from django.utils.translation import gettext_lazy as _

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
@authenticated_view
def settings_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/settings.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")


@api_view(['GET'])
@authenticated_view
def current_user(request):
    user = request.user
    try:
        email_verified = EmailAddress.objects.get(user=user, primary=True) is not None
    except ObjectDoesNotExist:
        email_verified = False
    
    profile = user.profile
    active_tournament = UserActiveTournament.objects.filter(user=user).first()
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
        },
        'active_tournament_id': active_tournament.tournament.id if active_tournament.tournament else None,
    }
    return JsonResponse(data)

@require_GET
def custom_set_language(request):
    language = request.GET.get('language')
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

        response = JsonResponse({'status': 'success', 'language': language})
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid language')}, status=400)

@require_POST
def save_snow_intensity(request):
    intensity = request.POST.get('snowIntensity')
    if intensity is not None:
        try:
            intensity = int(intensity)
            request.user.profile.snowIntensity = intensity
            request.user.profile.save()
            return JsonResponse({'status': 'success'})

        except ValueError:
            return JsonResponse({'status': 'error', 'message': _('Invalid intensity value')}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': _('Invalid intensity value')}, status=400)