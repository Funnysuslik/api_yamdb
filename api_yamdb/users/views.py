from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

from users.permissions import IsAdmin
from users.serializers import (ForAdminSerializer, ForUserSerializer,
                               TokenSerializer)

from .models import User


class APISignUp(APIView):
    """User auth"""

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ForUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.create_confirmation_code_and_send_email(
                serializer.data['username'])
            return Response(
                {'email': serializer.data['email'],
                 'username': serializer.data['username']},
                status=status.HTTP_200_OK)

    @staticmethod
    def create_confirmation_code_and_send_email(username):
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=f'{user.username} Confirmation code',
            message=f'Your confirmation code {confirmation_code}',
            from_email=None,
            recipient_list=[user.email, ])


class APIToken(APIView):
    """Get token"""

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
            if default_token_generator.check_token(
                    user, serializer.data['confirmation_code']):
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK)
            return Response({
                'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """Работа с пользователями"""
    permission_classes = (IsAdmin, )
    queryset = User.objects.all()
    serializer_class = ForAdminSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = ForUserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = ForAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = ForUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
