# views.py
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from utils.request_helpers import is_ajax_request
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET



User = get_user_model()

class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_num = request.GET.get('group_num')
        return Response({'group_num': group_num})

class FriendChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_num = request.GET.get('group_num')
        return Response({'group_num': group_num})

class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, receiver_id):
        receiver = get_object_or_404(User, id=receiver_id)
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            chat_message = serializer.save(sender=request.user, receiver=receiver)
            return Response(ChatMessageSerializer(chat_message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receiver_id):
        receiver = get_object_or_404(User, id=receiver_id)
        messages = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) | 
            (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
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
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    serialized_messages = ChatMessageSerializer(messages, many=True).data
    print(f"Room Name: {room.get_room_name(request.user)}")
    
    # friend_username = request.GET.get('username')
    # if not friend_username:
    #     return HttpResponseBadRequest('Error: username field is required')
    # friend = get_object_or_404(User, username=friend_username)
    # print(ChatRoom.get_private_chat_roomname(request.user, friend))
    # room = get_object_or_404(ChatRoom, name=ChatRoom.get_private_chat_roomname(request.user, friend))
    # messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    # serialized_messages = ChatMessageSerializer(messages, many=True).data
    # print(f"Room Name: {room.get_room_name(request.user)}")
    
    
    return render(request, 'components/drawers/chat-room.html', {
        'room': room,
        'room_name': room.get_room_name(request.user),
        'messages': serialized_messages
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_friendroom_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    
    # room_id = request.GET.get('room_id')
    # if not room_id:
    #     return HttpResponseBadRequest("Error: Room ID is required.")
    
    # room = get_object_or_404(ChatRoom, id=room_id)


    # private chat of request.user with request.data.get('username')
    # get room_id of this private room
    friend_username = request.GET.get('username')
    if not friend_username:
        return HttpResponseBadRequest('Error: username field is required')
    friend = get_object_or_404(User, username=friend_username)
    
    # print(ChatRoom.get_private_chat_roomname(request.user, friend))
    room = get_object_or_404(ChatRoom, name=ChatRoom.get_private_chat_roomname(request.user, friend))
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
    serialized_messages = ChatMessageSerializer(messages, many=True).data
    print(f"Room Name: {room.get_room_name(request.user)}")
    
    
    # Debug output
    print(f"Messages count: {messages.count()}")
    print(f"Serialized messages: {serialized_messages}")
    return render(request, 'components/drawers/chat-friendroom.html', {
        'room': room,
        # 'room_name': 'no way',
        'room_name': room.get_room_name(request.user),
        'messages': serialized_messages
    })
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def chat_friendroom_drawer(request):
#     if not is_ajax_request(request):
#         return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    
#     friend_username = request.GET.get('username')
#     if not friend_username:
#         return HttpResponseBadRequest("Error: 'username' parameter is required.")
    
#     friend = get_object_or_404(User, username=friend_username)
#     room_name = ChatRoom.get_private_chat_roomname(request.user, friend)
#     room = get_object_or_404(ChatRoom, name=room_name)
    
#     messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')
#     serialized_messages = ChatMessageSerializer(messages, many=True).data
    
#     # Render the HTML content for the drawer
#     content = render_to_string('components/drawers/chat-friendroom.html', {
#         'room': room,
#         'room_name': room.get_room_name(request.user),
#         'messages': serialized_messages
#     }, request=request)
    
#     return JsonResponse({'html': content})

# @require_GET
# def get_chat_messages(request, room_id):
#     try:
#         chat_room = ChatRoom.objects.get(id=room_id)
#         messages = chat_room.chat_messages.all().order_by('timestamp')
#         messages_data = [
#             {
#                 'sender': message.sender.username,
#                 'receiver': message.receiver.username if message.receiver else 'No Receiver',
#                 'message': message.message,
#                 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#             }
#             for message in messages
#         ]
#         return JsonResponse({'messages': messages_data})
#     except ChatRoom.DoesNotExist:
#         return JsonResponse({'error': 'Chat room not found'}, status=404)
    
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import ChatRoom, ChatMessage

# def fetch_chat_messages(request, room_id):
#     room = get_object_or_404(ChatRoom, id=room_id)
#     messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    
#     # Serialize the messages into a list of dictionaries
#     messages_data = []
#     for message in messages:
#         messages_data.append({
#             'sender': message.sender.username,
#             'receiver': message.receiver.username if message.receiver else 'No Receiver',
#             'message': message.message,
#             'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#         })
    
#     return JsonResponse({'messages': messages_data})
def fetch_chat_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')

    # Serializing the message data
    messages_data = [
        {
            'sender': message.sender.username,
            'receiver': message.receiver.username if message.receiver else 'No Receiver',
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for message in messages
    ]

    return JsonResponse({'messages': messages_data})

# ---------------------------------------------------------------------------------------------------------------------------------------

from django.core.paginator import Paginator
def get_paginated_messages(request, room_id):
    print(f"get_paginated_messages called")
    print(f"Room ID: {room_id}")
    page = request.GET.get('page', 1)  # Get the current page number from the request
    per_page = request.GET.get('per_page', 20)  # Number of messages per page

    messages = ChatMessage.objects.filter(room_id=room_id).order_by('-timestamp')  # Order by latest messages

    paginator = Paginator(messages, per_page)
    current_page = paginator.get_page(page)

    # Serialize the messages
    message_list = [
        {
            'sender': message.sender.username,
            'receiver': message.receiver.username if message.receiver else 'everyone',
            'message': message.message,
            'timestamp': message.timestamp.isoformat(),
        }
        for message in current_page
    ]

    return JsonResponse({
        'messages': message_list,
        'has_previous': current_page.has_previous(),
        'has_next': current_page.has_next(),
        'current_page': current_page.number,
        'total_pages': paginator.num_pages,
    })
