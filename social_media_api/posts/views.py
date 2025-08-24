from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    user = request.user
    #Get posts from users that the current user follows
    posts = Post.objects.filter(author__in=user.following.all()).order_by('-created_at')
    serialize = PostSerialize(posts, many=True)
    return Response(serializer.data)
      
    
      


