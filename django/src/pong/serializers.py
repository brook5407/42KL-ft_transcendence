from rest_framework import serializers
from .models import Player, TournamentRoom, Match, TournamentPlayer, TournamentMatch


class TournamentRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentRoom
        fields = [
            "id",
            "name",
            "description",
            "players",
            "winner",
            "matches",
            "status",
            "ended_at",
            "created_at",
        ]


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
