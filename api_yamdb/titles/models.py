from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator  # , MinValueValidator
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """not done yet"""
    somefield = models.TextField(
        'some description',
        blank=True,
    )


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
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    created = models.DateTimeField(
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
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField
    created = models.DateTimeField(
        'Creation date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:

        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text[:10]




"""
class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ID отзыва',
    )
    text = models.TextField(
        'Текст отзыва',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Username пользователя'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='ID комментария'
    )
    text = models.TextField(
        'Текст комментария',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Username автора комметария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

"""
