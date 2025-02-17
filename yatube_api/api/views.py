from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnlyPermission
from posts.models import Group, Post
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет управления комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission
    ]
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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyPermission
    ]

    def perform_create(self, serializer):
        """Создает объект автора."""
        serializer.save(author=self.request.user)

    def paginate_queryset(self, queryset):
        if (
            'limit' not in self.request.query_params
                and 'offset' not in self.request.query_params
        ):
            return None
        return super().paginate_queryset(queryset)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет управления подписчиками."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('=following__username',)
    # = меняет поиск с обычного на точное совпадение

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
