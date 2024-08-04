from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from chat.models import ChatMessage, ChatRoom
from chat.serializers import ChatMessageSerializer
from chat.pagination import ChatMessagePagination
from utils.request_helpers import is_ajax_request
from .models import Profile
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
@permission_classes([IsAuthenticated])
def profile_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/profile.html', {
            'profile': Profile.objects.get(user=request.user)
        })
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def settings_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/settings.html')
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list_drawer(request):
    if is_ajax_request(request):
        return render(request, 'components/drawers/chat-list.html', {
        'public_chats': ChatRoom.objects.filter(is_public=True),
        'private_chats': ChatRoom.get_private_chats(request.user)
	})
    return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_room_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")

    room_id = request.GET.get('room_id')
    if not room_id:
        return HttpResponseBadRequest("Error: Room ID is required.")
    
    room = get_object_or_404(ChatRoom, id=room_id)
    # messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    
    return render(request, 'components/drawers/chat-room.html', {
        'room': room,
        'room_name': room.get_room_name(request.user),
        # 'messages': ChatMessageSerializer(messages, many=True).data
    })