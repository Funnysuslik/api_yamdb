from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from yatube_api.settings import (MESSAGE_FOR_RESERVED_NAME,
                                 RESERVED_NAME)


class MyUserManager(UserManager):
    """Сохраняет пользователя только с email.
    Зарезервированное имя использовать нельзя."""

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательное')
        if username == RESERVED_NAME:
            raise ValueError(MESSAGE_FOR_RESERVED_NAME)
        return super().create_user(
            username, email, password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    ROLES_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    # email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=50, choices=ROLES_CHOICES, default='user')
    username = models.CharField(max_length=50, unique=True)  # , db_index=True)

    objects = MyUserManager()

    # A list of the field names that will be prompted
    # for when creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ROLES_CHOICES[2][1]

    @property
    def is_moderator(self):
        return self.role == self.ROLES_CHOICES[1][1]

    @property
    def is_user(self):
        return self.role == self.ROLES_CHOICES[0][1]
