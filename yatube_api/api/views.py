from rest_framework import status, viewsets
from rest_framework.response import Response

from posts.models import Comment, Group, Post

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post=post_id)[-'created']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_destroy(instance)
