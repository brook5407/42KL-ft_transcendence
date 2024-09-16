# models.py
from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


class Player(BaseModel):
    """
    Range for Matching:
    You can define a range of acceptable Elo ratings for matching players,
    e.g., match players with others within ±100 Elo points.
    As the waiting time increases, you can expand the range.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        null=True,
        blank=True,
        related_name="player",
    )
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    elo = models.IntegerField(default=1200)

    """
        ELO Rating System:

        Ea = 1 / (1 + 10^((Rb - Ra) / 400))
        Eb = 1 / (1 + 10^((Ra - Rb) / 400))
        Ra' = Ra + K * (Sa - Ea)
        Rb' = Rb + K * (Sb - Eb)
        where:
            - Ra and Rb are the ratings of players A and B, respectively.
            - Ea and Eb are the expected scores of players A and B, respectively.
            - K is the weight constant (e.g., 32 for chess).
        In tournament play, just add/sub a fixed value (e.g. 32) to the winner/loser.

    """

    def __str__(self):
        return f"{self.user.username}"


class Match(BaseModel):
    class MatchType(models.TextChoices):
        PVP = "P", "PVP"
        PVE = "E", "PVE"

    winner = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="match_winner"
    )
    loser = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="match_loser"
    )
    winner_score = models.IntegerField(default=0)
    loser_score = models.IntegerField(default=0)
    type = models.CharField(
        max_length=1, choices=MatchType.choices, null=True, blank=True
    )
    ended_at = models.DateTimeField(null=True, blank=True)
    history = GenericRelation("MatchHistory", related_query_name="match_history")

    def __str__(self):
        return f"{self.winner} vs {self.loser}. winner: {self.winner}"


class TournamentRoom(BaseModel):
    MAX_PLAYERS = 8

    class Status(models.TextChoices):
        WAITING = "W", "Waiting"
        ONGOING = "O", "Ongoing"
        COMPLETED = "C", "Completed"

    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    players = models.ManyToManyField(
        "TournamentPlayer", related_name="tournament_players"
    )
    winner = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        related_name="tournament_winner",
        null=True,
        blank=True,
    )
    matches = models.ManyToManyField(
        "TournamentMatch", related_name="tournament_matches"
    )
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.WAITING
    )
    ended_at = models.DateTimeField(null=True, blank=True)
    history = GenericRelation("MatchHistory", related_query_name="tournament_history")

    def __str__(self):
        return f"Tournament: {self.name}"


class TournamentPlayer(BaseModel):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="tournament_player"
    )
    position = models.IntegerField(default=0)
    tournament = models.ForeignKey(
        TournamentRoom, on_delete=models.CASCADE, related_name="tournament_player"
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.player}: Player {self.position} in {self.tournament}"


class TournamentMatch(BaseModel):
    winner = models.ForeignKey(
        TournamentPlayer,
        on_delete=models.SET_NULL,
        related_name="tournament_match_winner",
        null=True,
        blank=True,
    )
    loser = models.ForeignKey(
        TournamentPlayer,
        on_delete=models.SET_NULL,
        related_name="tournament_match_loser",
        null=True,
        blank=True,
    )
    winner_score = models.IntegerField(default=0)
    loser_score = models.IntegerField(default=0)
    tournament = models.ForeignKey(
        TournamentRoom, on_delete=models.CASCADE, related_name="tournament_match"
    )

    def __str__(self):
        return f"{self.winner} vs {self.loser}. winner: {self.winner}"


class MatchHistory(BaseModel):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="match_history_player"
    )
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="match_history_match"
    )
    elo_change = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.player} in {self.match}. Elo change: {self.elo_change}"
