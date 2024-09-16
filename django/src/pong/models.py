# models.py
from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


class Player(BaseModel):
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
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="owner")
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

    def save(self, *args, **kwargs):
        if self.players.count() >= self.MAX_PLAYERS:
            raise ValueError("Maximum number of players exceeded.")
        super().save(*args, **kwargs)

    def add_player(self, user, position):
        if position > self.MAX_PLAYERS:
            raise ValueError("Maximum number of players exceeded.")
        try:
            player = Player.objects.get(user=user)
            tournament_player = TournamentPlayer.objects.create(
                player=player, tournament=self, position=position
            )
        except (Player.DoesNotExist, TournamentPlayer.DoesNotExist):
            raise ValueError("Player or TournamentPlayer does not exist.")
        self.players.add(tournament_player)

    def remove_player(self, user):
        try:
            player = Player.objects.get(user=user)
            tournament_player = TournamentPlayer.objects.get(
                player=player, tournament=self
            )
        except (Player.DoesNotExist, TournamentPlayer.DoesNotExist):
            raise ValueError("Player or TournamentPlayer does not exist.")
        # reposition players
        for player in self.players.all():
            if player.position > tournament_player.position:
                player.position -= 1
                player.save()
        self.players.remove(tournament_player)

    def is_member(self, user):
        try:
            player = Player.objects.get(user=user)
            tournament_player = TournamentPlayer.objects.get(
                player=player, tournament=self
            )
        except (Player.DoesNotExist, TournamentPlayer.DoesNotExist):
            return False
        return self.players.filter(player=tournament_player).exists()

    def is_owner(self, user):
        return self.owner.user == user

    def start(self):
        self.status = self.Status.ONGOING
        self.save()

    def end(self):
        self.status = self.Status.COMPLETED
        self.save()

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
