from django.shortcuts import render
from utils.request_helpers import is_ajax_request, authenticated_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)
from asgiref.sync import async_to_sync
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Player, TournamentRoom, Match, TournamentPlayer, UserActiveTournament
from .serializers import (
    TournamentRoomSerializer,
    TournamentRoomCreateSerializer,
    MatchSerializer,
)
from django.contrib.auth.decorators import login_required


@api_view(["GET"])
@authenticated_view
def pvp_view(request):
    if is_ajax_request(request):
        match_id = request.GET.get("match_id")
        if match_id:
            return render(request, "components/pages/pong.html", {"game_mode": "pvp", "match_id": match_id})
        return render(request, "components/pages/pong.html", {"game_mode": "pvp"})
    return render(request, "index.html")


@api_view(["GET"])
@authenticated_view
def pve_view(request):
    match = Match.objects.create()
    if is_ajax_request(request):
        return render(request, "components/pages/pong.html", {"game_mode": "pve", "match_id": match.id})
    return render(request, "index.html")

@api_view(["GET"])
@authenticated_view
def tournament_view(request):
    if is_ajax_request(request):
        tournament_id = request.GET.get("tournament_id")
        return render(request, "components/pages/pong.html", {
            "game_mode": "tournament",
            "tournament_id": tournament_id
        })
    return render(request, "index.html")

@api_view(["GET"])
@authenticated_view
def tournament_list_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest(
            "Error: This endpoint only accepts AJAX requests."
        )
    user_active_tournament = UserActiveTournament.objects.get(user=request.user)
    if user_active_tournament.tournament is not None:
        serializer = TournamentRoomSerializer(user_active_tournament.tournament)
        return render(request, "components/drawers/pong/tournament/room.html", context={
            "tournament_room": serializer.data
        })
    return render(request, "components/drawers/pong/tournament/list.html")

@api_view(["GET"])
@authenticated_view
def tournament_room_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest(
            "Error: This endpoint only accepts AJAX requests."
        )
    tournament_room_id = request.GET.get("tournament_room_id")
    if not tournament_room_id:
        return HttpResponseBadRequest("Error: tournament_room_id is required.")
    tournament_room = get_object_or_404(TournamentRoom, pk=tournament_room_id)
    serializer = TournamentRoomSerializer(tournament_room)
    return render(request, "components/drawers/pong/tournament/room.html", context={
        "tournament_room": serializer.data
    })

@api_view(["GET"])
@authenticated_view
def tournament_create_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest(
            "Error: This endpoint only accepts AJAX requests."
        )
    return render(request, "components/drawers/pong/tournament/create.html")


class TournamentRoomViewSet(viewsets.ModelViewSet):
    queryset = TournamentRoom.objects.filter(status=TournamentRoom.Status.WAITING)
    serializer_class = TournamentRoomSerializer

    @action(detail=False, methods=["GET"])
    def shuffle(self, request):
        queryset = self.get_queryset().order_by("?")[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def details(self, request, pk=None):
        tournament_room = get_object_or_404(TournamentRoom, pk=pk)
        serializer = self.get_serializer(tournament_room)
        return Response(serializer.data)

    def create(self, request):
        active_tournament = UserActiveTournament.objects.get(user=request.user)
        if active_tournament.tournament is not None:
            return Response(
                {"detail": "You are already in a tournament room."},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = TournamentRoomCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        tournament_room = serializer.save()
        active_tournament.tournament = tournament_room
        active_tournament.save()
        return Response(tournament_room.id, status=HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def join(self, request, pk=None):
        tournament_room = get_object_or_404(TournamentRoom, pk=pk)
        active_tournament = UserActiveTournament.objects.get(user=request.user)
        if active_tournament.tournament is not None:
            return Response(
                {"detail": "You are already in a tournament room."},
                status=HTTP_400_BAD_REQUEST,
            )
        if tournament_room.players.count() >= TournamentRoom.MAX_PLAYERS:
            return Response(
                {"detail": "The tournament room is full."}, status=HTTP_400_BAD_REQUEST
            )
        tournament_room.add_player(request.user)
        active_tournament.tournament = tournament_room
        active_tournament.save()
        return Response(status=HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def leave(self, request, pk=None):
        tournament_room = get_object_or_404(TournamentRoom, pk=pk)
        if tournament_room.is_owner(request.user):
            tournament_room.delete()
        elif tournament_room.is_member(request.user):
            tournament_room.remove_player(request.user)
        else:
            return Response(
                {"detail": "You are not a member of this tournament room."},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            active_tournament = UserActiveTournament.objects.get(user=request.user)
            active_tournament.tournament = None
            active_tournament.save()
        except UserActiveTournament.DoesNotExist:
            pass
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def start(self, request, pk=None):
        tournament_room = get_object_or_404(TournamentRoom, pk=pk)
        if not tournament_room.is_owner(request.user):
            return Response(
                {"detail": "You are not the owner of this tournament room."},
                status=HTTP_400_BAD_REQUEST,
            )
        tournament_room.start()
        return Response(status=HTTP_200_OK)


class PongInvitationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["POST"])
    def invite(self, request):
        pass
    
    @action(detail=True, methods=["POST"])
    def accept(self, request, pk=None):
        pass
    
    @action(detail=True, methods=["POST"])
    def reject(self, request, pk=None):
        pass