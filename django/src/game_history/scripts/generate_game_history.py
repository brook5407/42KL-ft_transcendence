# scripts/generate_game_history.py
import random
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from ..models import GameHistory


User = get_user_model()

def get_or_create_users():
    user1, _ = User.objects.get_or_create(username="brook5407")
    user2, _ = User.objects.get_or_create(username="l3rook")
    return user1, user2


def generate_game_history(user1, user2, num_games):
    start_date = datetime.now() - timedelta(days=30)  # Generate games for the last 30 days

    for _ in range(num_games):
        score1 = random.randint(0, 5)
        score2 = random.randint(0, 5)
        winner = user1 if score1 > score2 else user2
        game_date = datetime.today()

        GameHistory.objects.create(
            player1=user1,
            player2=user2,
            winner=winner,
            score_player1=score1,
            score_player2=score2,
            game_date=game_date
        )


def run():
    num_games = 5  # Adjust this number as needed

    print("Getting or creating users...")
    user1, user2 = get_or_create_users()

    print(f"Generating {num_games} game history entries for {user1.username} and {user2.username}...")
    generate_game_history(user1, user2, num_games)

    print("Sample game history generated successfully!")

    # Print some sample data
    print("\nSample Game History:")
    for game in GameHistory.objects.filter(player1__username__in=["brook5407", "l3rook"]).order_by('-game_date')[:5]:
        print(f"{game.player1.username} vs {game.player2.username} - "
              f"Score: {game.score_player1}-{game.score_player2} - "
              f"Winner: {game.winner.username} - Date: {game.game_date}")
