from rest_framework import serializers
from .models import Player, TournamentRoom, Match, TournamentPlayer, TournamentMatch


class TournamentRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentRoom
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "players",
            "winner",
            "matches",
            "status",
            "ended_at",
            "created_at",
        ]


class TournamentRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentRoom
        fields = [
            "name",
            "description",
        ]

    def create(self, validated_data):
        owner = self.context["request"].user
        owner_player = Player.objects.get(user=owner)
        tournament_room = TournamentRoom.objects.create(
            owner=owner_player, **validated_data
        )
        return tournament_room


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "elo", "created_at"]


class MatchSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = TournamentPlayer
        fields = ["id", "player", "position", "tournament", "created_at"]


class TournamentMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentMatch
        fields = [
            "id",
            "winner",
            "loser",
            "winner_score",
            "loser_score",
            "tournament",
            "created_at",
        ]
