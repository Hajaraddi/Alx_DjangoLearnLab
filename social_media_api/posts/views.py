from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.response import Response


CustomUser = get_user_model()

class FeedView(generics.GenericsAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        #get the users the current user is following
        following_users = request.user.following.all()

        #filter posts fro those users, order by newset first
        posts = Post.objects.filter(author_in=following_users).order_by('-created_at')

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)



      








class IsOwnerOrReadyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # write permissions only for owners
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-crated_at")
    serializer_class = PostSerializer
    permisson_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadyOnly]
    #Added 👇
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelView):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadyOnly]

    def perfom_create(self, serializer):
        serializer.save(author=self.request.us)

    
      


