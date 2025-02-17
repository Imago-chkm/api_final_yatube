from rest_framework.pagination import LimitOffsetPagination


class PostViewSetPagination(LimitOffsetPagination):
    """Опциональное включение пагинации для PostViewSet."""

    def paginate_queryset(self, queryset, request, view=None):
        if (
            'limit' not in request.query_params
                and 'offset' not in request.query_params
        ):
            return None
        return super().paginate_queryset(queryset, request, view)
