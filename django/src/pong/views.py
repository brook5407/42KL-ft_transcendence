from django.shortcuts import render, redirect
from utils.request_helpers import is_ajax_request
from django.contrib.auth.decorators import login_required
import uuid
# from .models import GameRoom

@login_required
def pong(request):
    if is_ajax_request(request):
        return render(request, 'components/pages/pong.html')
    return render(request, 'index.html')

# def pong_game_view(request, room_name):
#     return render(request, 'components/pages/pong.html', {'room_name': room_name})

# def find_or_create_room(request):
#     # Look for an existing room that needs a second player
#     room = GameRoom.objects.filter(player2__isnull=True).first()
    
#     if not room:
#         # No room available, create a new one with a unique name
#         room_name = str(uuid.uuid4())  # Generate a unique room name
#         room = GameRoom.objects.create(room_name=room_name, player1=request.user)
#     else:
#         # Assign the current user as the second player in the found room
#         room.player2 = request.user
#         room.save()

#     # Redirect to the game room
#     return redirect(f'/pong/{room.room_name}/')
