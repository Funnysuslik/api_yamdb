from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import mixins


from reviews.models import Review, Title, Category, Genre
from users.permissions import IsAuthorOrAdministratorOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
)


# class CustomMixin(ListModelMixin, CreateModelMixin, DestroyModelMixin,
#                   viewsets.GenericViewSet):
#     pass


class CategoryViewSet(viewsets.ModelViewSet):  # (CustomMixin):
    """API для работы с моделью категорий."""
    # pagination_class = LimitOffsetPagination
    # permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):  # (CustomMixin):
    """API для работы с моделью жанров."""
    # pagination_class = LimitOffsetPagination
    # permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """API для работы с моделью произведений."""
    # pagination_class = LimitOffsetPagination
    # permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = TitleFilter
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not Title.objects.filter(pk=self.kwargs.get('title_id')).exists():

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        if Review.objects.filter(author=self.request.user, title=self.kwargs.get('title_id')).exists():
            
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        title = Title.objects.get(pk=self.kwargs.get('title_id'))
        
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for comments model."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not (
            Title.objects.filter(pk=self.kwargs.get('title_id')).exists() or
            Review.objects.filter(pk=self.kwargs.get('review_id')).exists()   
        ):

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        review = Review.objects.get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
