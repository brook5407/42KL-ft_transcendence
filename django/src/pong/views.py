from django.shortcuts import render, redirect
from utils.request_helpers import is_ajax_request
from django.contrib.auth.decorators import login_required
import uuid
from .models import GameRoom

def generate_room_name():
    return str(uuid.uuid4())[:4]  # Generate a short unique identifier

# @login_required
def pong(request):
    available_room = GameRoom.objects.filter(is_full=False).first()

    if available_room:
        room_name = available_room.room_name
        available_room.is_full = True
        available_room.save()
    else:
        room_name = generate_room_name()
        GameRoom.objects.create(room_name=room_name)

    return render(request, 'components/pages/pong.html', {'room_name': room_name})
    # if is_ajax_request(request):
    #     return render(request, 'components/pages/pong.html', {'room_name': room_name})
    # return render(request, 'index.html')
