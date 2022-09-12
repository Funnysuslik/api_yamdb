"""Serializers."""
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Comment, Review


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for comment db model."""


    class Meta:
        """Filler."""

        fields = ('text',)
        model = Comment


class ReviewsSerializer(serializers.ModelSerializer):
    """Serializer for review db model."""

    class Meta:
        """Filler."""

        fields = ('text', 'score')
        model = Review        
