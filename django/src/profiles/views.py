from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import ProfileSerializer
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_edit_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/profile-edit.html', {
            'profile': Profile.objects.get(user=request.user)
        })
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, serializers.ValidationError):
            response.data = {
                'non_field_errors': response.data.get('non_field_errors', []),
                **{field: messages for field, messages in response.data.items() if field != 'non_field_errors'}
            }
        return response