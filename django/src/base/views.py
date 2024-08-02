from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from utils.request_helpers import is_ajax_request
from .models import Profile
from rest_framework.decorators import api_view, permission_classes


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
        return render(request, 'components/modals/signin.html')
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
def profile_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/profile.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
def settings_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/settings.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")