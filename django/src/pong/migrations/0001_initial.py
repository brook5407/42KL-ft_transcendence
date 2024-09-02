# Generated by Django 5.0.3 on 2024-09-02 01:17

import base.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRoom',
            fields=[
                ('id', base.fields.RandomStringIDField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('room_name', models.CharField(max_length=8, unique=True)),
                ('is_full', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MatchHistory',
            fields=[
                ('id', base.fields.RandomStringIDField(editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('won', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('opponent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_matches', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_matches', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
