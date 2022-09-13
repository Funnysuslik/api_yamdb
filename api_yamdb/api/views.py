from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from reviews.models import Category, Genre, Review, Title
from users.permissions import (IsAdminOrReadOnly,
                               IsAuthorOrAdministratorOrReadOnly)

from .filters import TitleFilter
from .serializers import (CategoriesSerializer, CategorySerializer,
                          CommentsSerializer, GenreSerializer,
                          ReviewsSerializer, TitleCreateSerializer,
                          TitleSerializer)

# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import mixins


class GenCatMix(mixins.ListModelMixin, mixins.CreateModelMixin,
                mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    pagination_class = (LimitOffsetPagination,)


class GenreViewSet(GenCatMix):
    """ Получить список жанров может любой пользователь.
    Добавление и удаление жанра доступно только админу."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenCatMix):
    """ Получить список категорий может любой пользователь.
    Добавление и удаление категорий доступно только админу."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    paginathion_class = (LimitOffsetPagination,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitleSerializer
        return TitleCreateSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = CategoriesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for comments model."""

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
