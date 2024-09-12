from rest_framework import serializers
from .models import GameHistory


class GameHistorySerializer(serializers.ModelSerializer):
    player1_username = serializers.ReadOnlyField(source='player1.username')
    player2_username = serializers.ReadOnlyField(source='player2.username')
    winner_username = serializers.ReadOnlyField(source='winner.username')

    class Meta:
        model = GameHistory
        fields = ['id', 'player1', 'player2', 'winner', 'score_player1', 'score_player2',
                  'created_at', 'player1_username', 'player2_username', 'winner_username']
        read_only_fields = ['id', 'created_at']

