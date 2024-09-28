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
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model


User = get_user_model()


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
    player = Player.objects.get(user=request.user)
    ai_player = Player.objects.get(user__username="aiskosong")
    match = Match.objects.create(
        winner=player,
        loser=ai_player,
        type=Match.MatchType.PVE
    )
    if is_ajax_request(request):
        return render(request, "components/pages/pong.html", {"game_mode": "pve", "match_id": match.id})
    return render(request, "index.html")

@api_view(["GET"])
@authenticated_view
def local_view(request):
    player = Player.objects.get(user=request.user)
    ai_player = Player.objects.get(user__username="aiskosong")
    match = Match.objects.create(
        winner=player,
        loser=ai_player,
        type=Match.MatchType.PVE
    )
    if is_ajax_request(request):
        return render(request, "components/pages/pong.html", {"game_mode": "local", "match_id": match.id})
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

@api_view(['GET'])
@authenticated_view
def match_history_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    username = request.GET.get('username')
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    return render(request, 'components/drawers/game-history.html', context={
        'user': user
    })


class MatchHistoryViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by("-ended_at")

    def list(self, request):
        username = request.query_params.get("username")
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        player = Player.objects.get(user=user)
        queryset = self.queryset.filter(
            Q(winner=player) | Q(loser=player)
        )
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the page size as needed
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize the paginated queryset
        serializer = MatchSerializer(paginated_queryset, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=["GET"])
    def details(self, request, pk=None):
        match = get_object_or_404(Match, pk=pk)
        serializer = MatchSerializer(match)
        return Response(serializer.data)


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