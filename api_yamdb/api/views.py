from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.response import Response


from reviews.models import Review, Title, Category, Genre
from users.permissions import (
    IsAuthorOrAdministratorOrReadOnly, IsAdminOrReadOnly)
from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class CustomMixin(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet):

    pass


class CategoryViewSet(CustomMixin):
    """API для работы с моделью категорий."""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CustomMixin):
    """API для работы с моделью жанров."""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """API для работы с моделью произведений."""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):

        if self.action in ('create', 'partial_update'):

            return TitleCreateSerializer

        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Title.objects.filter(pk=self.kwargs.get('title_id')).exists():

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        if Review.objects.filter(
            author=self.request.user,
            title=self.kwargs.get('title_id')
        ).exists():

            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        title = Title.objects.get(pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for comments model."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not (
            Title.objects.filter(pk=self.kwargs.get('title_id')).exists()
            or Review.objects.filter(pk=self.kwargs.get('review_id')).exists()
        ):

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        title = Title.objects.get(pk=self.kwargs.get('title_id'))
        review = title.reviews.get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
