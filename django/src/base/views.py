from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from chat.models import ChatMessage, ChatRoom
from chat.serializers import ChatMessageSerializer
from chat.pagination import ChatMessagePagination
from core import settings
from utils.request_helpers import is_ajax_request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
def current_user(request):
    user = request.user
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }
    return JsonResponse(user_data)
