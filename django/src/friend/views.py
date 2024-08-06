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

    @staticmethod
    def get(request):
        user = request.user
        user_relations = UserRelation.objects.filter(user=user, accepted=True)
        serializer = UserRelationSerializer(user_relations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request):
        username = request.data.get("username")
        user = request.user
        friend = get_object_or_404(User, username=username)

        try:
            user_relation = UserRelation.objects.get(user=user, friend=friend)
            user_relation.delete()
            UserRelation.objects.get(user=friend, friend=user).delete()
            return Response({"message": f"You have remove {username} from your friend list"}, status=status.HTTP_200_OK)
        except UserRelation.DoesNotExist:
            return Response({"message": f"{username} is not your friend anymore"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request):
        username = request.data.get("username")
        user = request.user
        friend = get_object_or_404(User, username=username)

        if UserRelation.objects.filter(user=user, friend=friend).exists():
            return Response({"message": f"You have sent {username} already"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRelationSerializer(data={
            "user": user.id,
            "friend": friend.id,
            "accepted": False
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Request sent to {username} successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        user_relations = UserRelation.objects.filter(friend=user, accepted=False)
        serializer = UserRelationSerializer(user_relations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        username = request.data.get("username")
        user = request.user
        friend = get_object_or_404(User, username=username)

        if UserRelation.objects.filter(user=user, friend=friend).exists():
            return Response({"message": f"You are friend with {username}"}, status=status.HTTP_400_BAD_REQUEST)

        user_relation = UserRelation.objects.create(user=user, friend=friend, accepted=True)
        friend_relation = UserRelation.objects.get(user=friend, friend=user)
        friend_relation.accepted = True
        friend_relation.save()

        return Response({"message": f"You have accepted friend request from {username}"}, status=status.HTTP_200_OK)

    