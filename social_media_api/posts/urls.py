
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, feed, FeedView, LikePostView, UnlikePostView
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path('feed/', FeedView.as_view(), name='user-feed'),
    path('<int:pk>/like/', LikePostView.as_View(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_View(), name='unlike-post'),
]



