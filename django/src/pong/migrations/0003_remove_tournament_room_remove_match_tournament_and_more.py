# Generated by Django 5.0.3 on 2024-09-17 03:53

import base.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pong', '0002_gameroom_created_at_gameroom_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='room',
        ),
        migrations.RemoveField(
            model_name='match',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='match',
            name='is_full',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='room_name',
        ),
        migrations.AddField(
            model_name='match',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_loser', to='pong.player'),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='type',
            field=models.CharField(blank=True, choices=[('P', 'PVP'), ('E', 'PVE')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='elo',
            field=models.IntegerField(default=1200),
        ),
        migrations.AddField(
            model_name='player',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_winner', to='pong.player'),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MatchHistory',
            fields=[
                ('id', base.fields.RandomStringIDField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('elo_change', models.IntegerField(default=0)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_history_match', to='pong.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_history_player', to='pong.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TournamentPlayer',
            fields=[
                ('id', base.fields.RandomStringIDField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player', to='pong.player')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='TournamentMatch',
            fields=[
                ('id', base.fields.RandomStringIDField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('winner_score', models.IntegerField(default=0)),
                ('loser_score', models.IntegerField(default=0)),
                ('loser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournament_match_loser', to='pong.tournamentplayer')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournament_match_winner', to='pong.tournamentplayer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TournamentRoom',
            fields=[
                ('id', base.fields.RandomStringIDField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('W', 'Waiting'), ('O', 'Ongoing'), ('C', 'Completed')], default='W', max_length=1)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('matches', models.ManyToManyField(related_name='tournament_matches', to='pong.tournamentmatch')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='pong.player')),
                ('players', models.ManyToManyField(related_name='tournament_players', to='pong.tournamentplayer')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournament_winner', to='pong.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tournamentplayer',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_player', to='pong.tournamentroom'),
        ),
        migrations.AddField(
            model_name='tournamentmatch',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_match', to='pong.tournamentroom'),
        ),
        migrations.DeleteModel(
            name='GameRoom',
        ),
        migrations.DeleteModel(
            name='Tournament',
        ),
    ]
