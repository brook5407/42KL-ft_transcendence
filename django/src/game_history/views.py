from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from rest_framework.pagination import PageNumberPagination
from utils.request_helpers import is_ajax_request, authenticated_view
from .models import GameHistory
from .serializers import GameHistorySerializer
from .pagination import GameHistoryPagination


User = get_user_model()

class GameHistoryViewSet(viewsets.ModelViewSet):
    queryset = GameHistory.objects.all().order_by('-created_at')
    serializer_class = GameHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GameHistoryPagination

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = self.request.user
        return GameHistory.objects.filter(
            Q(player1=user) | Q(player2=user)
        ).order_by('-created_at')


@api_view(['GET'])
@authenticated_view
def game_history_drawer(request):
    if not is_ajax_request(request):
        return HttpResponseBadRequest("Error: This endpoint only accepts AJAX requests.")
    return render(request, 'components/drawers/game-history.html')