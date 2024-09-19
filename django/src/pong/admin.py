from django.contrib import admin
from .models import Player, Match, TournamentRoom, TournamentPlayer, TournamentMatch, MatchHistory, UserActiveTournament
# Register your models here.

admin.site.register(Player)
admin.site.register(Match)
admin.site.register(TournamentRoom)
admin.site.register(TournamentPlayer)
admin.site.register(TournamentMatch)
admin.site.register(MatchHistory)
admin.site.register(UserActiveTournament)
