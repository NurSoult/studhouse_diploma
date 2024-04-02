from django.core.cache import cache
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import User, UserInfo
from ..serializers.user import UserSerializer, UserInfoSerializer, UserUpdateSerializer, UserCreateSerializer, \
    AddAdditionalUserSerializer
from ..utils import send_activation_code, check_activation_code


class UserCreateService:
    @staticmethod
    def user_create(request):
        password = request.data.get('password')

        try:
            with transaction.atomic():
                user_serializer = UserCreateSerializer(data=request.data)
                user_serializer.is_valid(raise_exception=True)
                user = User.objects.create_user(**user_serializer.validated_data)

                user.is_active = False
                user.set_password(password)
                user.save()

                UserInfo.objects.create(user=user)

                send_activation_code('user_activation', user.login)

                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def user_info_create(request):
        try:
            request.data['user'] = User.objects.get(id=request.data.get('user')).id
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_403_FORBIDDEN)

        user_info_serializer = UserInfoSerializer(data=request.data, partial=True)
        user_info_serializer.is_valid(raise_exception=True)
        user_info_serializer.save()

        return Response(user_info_serializer.data, status=status.HTTP_201_CREATED)


class UserUpdateService:
    @staticmethod
    def user_update(request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['pk'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_403_FORBIDDEN)

        user_serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        user_info = UserInfo.objects.filter(user=user).first()

        if not user_info:
            user_info = UserInfo.objects.create(user=user)

        user_info_serializer = UserInfoSerializer(user_info, data=request.data, partial=True)
        user_info_serializer.is_valid(raise_exception=True)
        user_info_serializer.save()

        if 'photo_avatar' in request.data:
            user_info.photo_avatar = request.data['photo_avatar']
            user_info.save()

        return Response(UserSerializer(user).data)


class AddAdditionalUserService:
    @staticmethod
    def add_additional_user(request):
        request.data['user'] = request.user.id

        add_additional_user_serializer = AddAdditionalUserSerializer(data=request.data)
        add_additional_user_serializer.is_valid(raise_exception=True)
        add_additional_user_serializer.save()

        return Response(add_additional_user_serializer.data, status=status.HTTP_201_CREATED)


class UserActivateService:
    @staticmethod
    def send_activation_code_to_login(login, resp_text):
        if not login:
            return Response({'error': 'Login is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(login=login).exists():
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        send_activation_code('user_activation', login)

        return Response({'message': resp_text}, status=status.HTTP_200_OK)

    def send_activation_code(self, request):
        return self.send_activation_code_to_login(request.data.get('login'), 'Activation code sent')

    @staticmethod
    def user_activate(request):
        login = request.data.get('login')
        code = request.data.get('code')

        if not login or not code:
            return Response({'error': 'Login or code is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(login=login).exists():
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(login=login)

        if user.is_active:
            return Response({'error': 'User already activated'}, status=status.HTTP_400_BAD_REQUEST)

        if check_activation_code('user_activation', login, int(code)) is False:
            return Response({'error': 'Incorrect code'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        token_data = TokenObtainPairSerializer()

        data = {
            'refresh': str(token_data.get_token(user)),
            'access': str(token_data.get_token(user).access_token)
        }

        cache.delete(f'user_activation_{user.id}')

        return Response(data, status=status.HTTP_200_OK)

    def send_reset_password_code(self, request):
        return self.send_activation_code_to_login(request.data.get('login'), 'Reset password code sent')

    @staticmethod
    def check_reset_password_code(request):
        login = request.data.get('login')
        code = request.data.get('code')

        if not login or not code:
            return Response({'error': 'Login or code is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(login=login).exists():
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if check_activation_code('user_reset_password', login, int(code)) is False:
            return Response({'error': 'Incorrect code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Code is correct'}, status=status.HTTP_200_OK)

    @staticmethod
    def reset_password(request):
        login = request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response({'error': 'Login or password is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(login=login).exists():
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(login=login)
        user.set_password(password)
        user.save()

        cache.delete(f'user_reset_password_{user.id}')

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)