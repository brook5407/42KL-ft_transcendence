from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserRelation
from .serializers import UserRelationSerializer


@method_decorator(csrf_exempt, name='dispatch')
class FriendManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        username = request.data.get("username")
        user = request.user
        friend = get_object_or_404(User, username=username)

        try:
            user_relation = UserRelation.objects.get(user=user, friend=friend)
            user_relation.delete()
            UserRelation.objects.get(user=friend, friend=user).delete()
            return Response({"message": "Friend deleted successfully."}, status=status.HTTP_200_OK)
        except UserRelation.DoesNotExist:
            return Response({"message": "Request deleted successfully."}, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get("username")
        user = request.user
        friend = get_object_or_404(User, username=username)

        if UserRelation.objects.filter(user=user, friend=friend).exists():
            return Response({"message": "friend request exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRelationSerializer(data={
            "user": user.id,
            "friend": friend.id,
            "accepted": False
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Request sent successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class AcceptRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        user = request.user
        friend = get_object_or_404(User, username=username)

        if UserRelation.objects.filter(user=user, friend=friend).exists():
            return Response({"message": "Relation already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user_relation = UserRelation.objects.create(user=user, friend=friend, accepted=True)
        friend_relation = UserRelation.objects.get(user=friend, friend=user)
        friend_relation.accepted = True
        friend_relation.save()

        return Response({"message": "Friend added successfully."}, status=status.HTTP_200_OK)