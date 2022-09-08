from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins

from titles.models import Comment, Review
from .serializers import CommentsSerializer, ReviewsSerializer
from .permissions import IsAuthorOrModeratorOrReadOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
