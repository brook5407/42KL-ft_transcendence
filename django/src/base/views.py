from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.request_helpers import is_ajax_request
from .models import Profile
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login


@require_http_methods(["GET"])
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def home(request):
    if is_ajax_request(request):
        return render(request, 'components/pages/home.html')
    return render(request, 'index.html')

@require_http_methods(["GET"])
def signin_modal(request):
    if is_ajax_request(request):
        return render(request, 'components/modals/signin.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@require_http_methods(["GET"])
def signup_modal(request):
    if is_ajax_request(request):
        return render(request, 'components/modals/signup.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@require_http_methods(["POST"])
def signin(request):
    # Extracting form data
    username_or_email = request.POST.get('email-or-username')
    password = request.POST.get('password')

    # Assuming you have a method to find user by email if username_or_email is an email
    user = authenticate(request, username=username_or_email, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return JsonResponse({'status': 'success', 'message': 'You are now logged in.'}, status=200)
    else:
        # Return an 'invalid login' error message.
        return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'}, status=401)