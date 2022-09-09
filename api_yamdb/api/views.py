"""Views."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


from titles.models import Comment, Review, Review, Title
from .serializers import CommentsSerializer, ReviewsSerializer
#from .permissions import IsAuthorOrModeratorOrReadOnly



class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for reviews model."""

    serializer_class = ReviewsSerializer
    #permission_classes = [IsAuthorOrModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset for comments model."""
    
    serializer_class = CommentsSerializer
    #permission_classes = [IsAuthorOrModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
