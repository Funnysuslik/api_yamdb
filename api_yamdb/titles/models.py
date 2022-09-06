from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """not done yet"""
    somefield = models.TextField(
        'some description',
        blank=True,
    )


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
