"""Views."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from titles.models import Review, Title
from .permissions import IsAuthorOrModeratorOrReadOnly
from .serializers import (
    CommentsSerializer,
    ReviewsSerializer,
)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""
    
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
