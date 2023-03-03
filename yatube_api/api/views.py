from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from posts.models import Comment, Group, Post

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid(self):
            serializer.save(author=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        serializer = PostSerializer(data=request.data)
        post = get_object_or_404(Post, id=pk)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if post.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED
            )
        if post.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        comment_id = self.kwargs.get('comment_id')
        if comment_id:
            return Comment.objects.filter(id=comment_id, post_id=post_id)
        return Comment.objects.filter(post_id=post_id)

    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid(self):
            serializer.save(author=self.request.user, post=post)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, post_id, pk):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if comment.author != self.request.user:
            return Response(
                data={"detail": 'Нельзя изменять чужой комментарий'},
                status=status.HTTP_403_FORBIDDEN
            )
        if serializer.is_valid(self):
            serializer.save(author=request.user, post=post)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, post_id, pk):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                post=post,
                data=request.data
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id, pk):
        comment = get_object_or_404(Comment, id=pk)
        if not request.user.is_authenticated:
            return Response(
                data={"detail": 'Вы не авторизованы'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if comment.author != request.user:
            return Response(
                data={"detail": 'Нельзя удалить чужой комментарий'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
