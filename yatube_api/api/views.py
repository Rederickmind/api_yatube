from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        if serializer.is_valid(self):
            serializer.save(author=self.request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        post_id = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        comment_id = self.kwargs.get('comment_id')
        if comment_id:
            return Comment.objects.filter(id=comment_id, post_id=post_id)
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        if serializer.is_valid(self):
            serializer.save(author=self.request.user, post=post)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
