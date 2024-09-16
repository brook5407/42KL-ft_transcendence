from django.shortcuts import render
from utils.request_helpers import is_ajax_request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from .models import Player, TournamentRoom, Match
from .serializers import TournamentRoomSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pvp_view(request):
    # WXR TODO: Implement the ELO rating system for matchmaking

    if is_ajax_request(request):
        return render(request, "components/pages/pong.html", {"game_mode": "pvp"})
    return render(request, "index.html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pve_view(request):
    if is_ajax_request(request):
        return render(request, "components/pages/pong.html", {"game_mode": "pve"})
    return render(request, "index.html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tournament_list_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest(
            "Error: This endpoint only accepts AJAX requests."
        )
    return render(request, "components/drawers/pong/tournament/list.html")


class TournamentRoomViewSet(viewsets.ModelViewSet):
    queryset = TournamentRoom.objects.all()
    serializer_class = TournamentRoomSerializer

    # WXR TODO: shuffle 5 random tournament rooms
    # WXR TODO: get tournament room details
    # WXR TODO: create tournament room
    # WXR TODO: join tournament room
    # WXR TODO: leave tournament room, destroy if is owner
    # WXR TODO: start tournament


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    # WXR TODO: matchmake (PVP)
    # WXR TODO: PVE
