from rest_framework import serializers
from base.serializers import UserSerializer
from .models import Player, TournamentRoom, Match, TournamentPlayer, UserActiveTournament, MatchInvitation


class TournamentRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentRoom
        fields = [
            "name",
            "description",
        ]

    def create(self, validated_data):
        # create tournament object and add owner as a player
        owner = self.context["request"].user
        tournament_room = TournamentRoom.objects.create(
            owner=owner, **validated_data
        )
        tournament_room.add_player(owner)
        return tournament_room


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ["id", "user", "wins", "losses", "elo", "created_at"]


class MatchSerializer(serializers.ModelSerializer):
    winner = PlayerSerializer(read_only=True)
    loser = PlayerSerializer(read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "winner",
            "loser",
            "winner_score",
            "loser_score",
            "type",
            "ended_at",
            "created_at",
        ]


class TournamentPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = TournamentPlayer
        fields = ["id", "player", "tournament", "last_match_at", "created_at"]


class TournamentRoomSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    players = TournamentPlayerSerializer(many=True, read_only=True)
    players_left = TournamentPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = TournamentRoom
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "players",
            "players_left",
            "winner",
            "matches",
            "status",
            "ended_at",
            "created_at",
        ]


class MatchInvitationSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = MatchInvitation
        fields = [
            "id",
            "sender",
            "receiver",
            "match",
            "status",
            "expired_at",
            "created_at",
        ]