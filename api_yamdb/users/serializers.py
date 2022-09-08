from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from yatube_api.settings import (MESSAGE_FOR_RESERVED_NAME,
                                 MESSAGE_FOR_USER_NOT_FOUND,
                                 RESERVED_NAME)

from .models import User

# когда взлетит эти два сериалайзера объединю


class ForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом user.
    Зарезервированное имя использовать нельзя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', )

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        return value


class ForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом admin.
    Зарезервированное имя использовать нельзя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена.
    Зарезервированное имя использовать нельзя."""
    username = serializers.CharField(max_length=50, required=True)
    confirmation_code = serializers.CharField(max_length=50, required=True)

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(MESSAGE_FOR_USER_NOT_FOUND)
        return value
