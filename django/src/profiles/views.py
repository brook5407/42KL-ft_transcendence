from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from utils.request_helpers import is_ajax_request
from .models import Profile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/profile.html', {
            'profile': Profile.objects.get(user=request.user)
        })
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")