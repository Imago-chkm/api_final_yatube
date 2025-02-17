from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from .pagination import PostViewSetPagination
from .permissions import IsAuthorOrReadOnlyPermission
from posts.models import Follow, Group, Post
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет управления комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_post(self):
        """Получение поста."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Фильтрация комментариев по post_id."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создает объект автора и поста."""
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )

    def perform_update(self, serializer):
        """Проверка прав на изменение контента."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """Проверка прав на удаление контента."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        return super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет управления группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = [IsAuthorOrReadOnlyPermission]


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет управления постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostViewSetPagination

    def perform_create(self, serializer):
        """Создает объект автора."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Проверка прав на изменение контента."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """Проверка прав на удаление контента."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        return super().perform_destroy(instance)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет управления подписчиками."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
