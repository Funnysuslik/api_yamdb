from rest_framework import serializers
from titles.models import Category, Comment, Genre, Review


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for comment db model."""

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewsSerializer(serializers.ModelSerializer):
    """Serializer for review db model."""

    class Meta:
        fields = '__all__'
        model = Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"
