from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from users.models import User


class NameSlug(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True
    )


class Category(NameSlug):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlug):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


def year():
    return timezone.now().year


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(
                year, 'Значение не должно быть больше текущей даты!'
            )
        ]
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг на основе отзывов',
        null=True,
        default=None
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """DB model for reviews."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        'Rating',
        validators=[
            MinValueValidator(1, 'Minimum value - 1'),
            MaxValueValidator(10, 'maximum value - 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Creation date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:

        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    """DB model for comments."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Creation date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:

        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text[:10]

# Еще один вариант моделей. 
# author, text, pub_date вынесены в отдельный класс.
"""
class ReviewComment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Creation date',
        auto_now_add=True,
        db_index=True
    )


class Review(ReviewComment):
    """DB model for reviews."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'Rating',
        validators=[
            MinValueValidator(1, 'Minimum value - 1'),
            MaxValueValidator(10, 'maximum value - 10')
        ]
    )

    class Meta:

        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.text[:10]


class Comment(ReviewComment):
    """DB model for comments."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:

        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text[:10]
"""
