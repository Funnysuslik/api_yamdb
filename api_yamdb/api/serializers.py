"""Serializers."""
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


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


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for category db model."""

    class Meta:
        """Filler."""

        fields = ('text', 'score')
        model = Category


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


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        exclude = ("id", )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug'
                                            )
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True
                                         )

    class Meta:
        model = Title
        exclude = ("id", )
