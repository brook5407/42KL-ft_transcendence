from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from utils.request_helpers import is_ajax_request
from django.contrib.auth.decorators import login_required
import uuid, secrets, string
from .models import Player, Tournament, Match, GameRoom

class RoomsManager:
    def __init__(self):
        self.rooms = {}

    def generate_room_name(self):
        length = 5
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(length))
    
    def create_room(self):
        room_name = self.generate_room_name()
        self.rooms[room_name] = {"players": []}  # Initialize room
        return room_name


@login_required
def pvp_view(request):
    # check for any avaliable room and assign second player to the same room
    available_room = GameRoom.objects.filter(is_full=False).first()

    if available_room:
        room_name = available_room.room_name
        available_room.is_full = True
        available_room.save()
    else:
        room_name = RoomsManager().create_room()
        GameRoom.objects.create(room_name=room_name)

    if is_ajax_request(request):
        return render(request, 'components/pages/pong.html', {
            'room_name': room_name,
            'game_mode': "pvp"
            })
    return render(request, 'index.html')

@login_required
def pve_view(request):
    room_name = RoomsManager().create_room()
    if is_ajax_request(request):
        return render(request, 'components/pages/pong.html', {
            'room_name': room_name,
            'game_mode': "pve"
            })
    return render(request, 'index.html')

@login_required
def tournament_view(request):
    if is_ajax_request(request):
        return render(request, 'components/pages/tournament_lobby.html')
    return render(request, 'index.html')

@login_required
def tournament_create_view(request):
    room_name = RoomsManager().create_room()
    redirect_url = reverse('pong.tournament_join', kwargs={'room_name': room_name})
    print(f"Generated room name: {room_name}, Redirect URL: {redirect_url}")  # Debug print
    return JsonResponse({'redirect_url': redirect_url})

@login_required
def tournament_join_view(request, room_name):
    print("tournament join view start")
    if is_ajax_request(request):
        return render(request, 'components/pages/tournament.html', {
            'room_name': room_name,
            'game_mode': "tournament"
            })
    return render(request, 'index.html')
