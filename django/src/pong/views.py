from django.shortcuts import render
from utils.request_helpers import is_ajax_request
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
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Player, TournamentRoom, Match, TournamentPlayer, TournamentMatch, UserActiveTournament
from .serializers import (
    TournamentRoomSerializer,
    TournamentRoomCreateSerializer,
    MatchSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pvp_view(request):
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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
        serializer = TournamentRoomCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        tournament_room = serializer.save()
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
        request.user.active_tournament = None
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
        # WXR TODO: trigger necessary events in the consumer
        return Response(status=HTTP_200_OK)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=["POST"])
    def matchmake(self, request):
        # WXR TODO: Implement the ELO rating system for matchmaking
        # Still need create unique room name before matchmaking
        pass

    @action(detail=False, methods=["POST"])
    def pve(self, request):
        # WXR TODO: start pve game
        pass
