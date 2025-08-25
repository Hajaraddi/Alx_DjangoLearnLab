from django.shortcuts import render
from rest_framework import status, permissions, generics 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
#create your views here
CustomUser = get_user_model()
class FollowUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,user_id):
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        if user_to_follow == request.user:
            return Response(
                {"detail" : "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.add(user_to_follow)
        return Response(
             {"detail": "You are now following {user_to_follow.username}."},
             statuts=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": f"You have unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )






    
    
