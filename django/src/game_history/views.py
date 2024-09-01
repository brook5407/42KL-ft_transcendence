from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from .models import GameHistory
from .serializers import GameHistorySerializer


User = get_user_model()

class GameHistoryViewSet(viewsets.ModelViewSet):
    queryset = GameHistory.objects.all().order_by('-game_date')
    serializer_class = GameHistorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        return GameHistory.objects.filter(
            Q(player1=user) | Q(player2=user)
        ).order_by('-game_date')

