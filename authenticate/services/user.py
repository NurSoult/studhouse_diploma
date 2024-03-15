from rest_framework import status
from rest_framework.response import Response

from ..models import User, UserRole, UserInfo
from ..serializers.user import UserSerializer, UserInfoSerializer, UserUpdateSerializer, UserCreateSerializer


class UserCreateService:
    @staticmethod
    def user_create(request):
        request_data = request.data.copy()
        try:
            request.data['role'] = UserRole.objects.get(id=request_data.pop('role')).id
        except UserRole.DoesNotExist:
            return Response({'message': 'Роль не найден!'}, status=status.HTTP_403_FORBIDDEN)

        user_serializer = UserCreateSerializer(data=request_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**user_serializer.validated_data)

        user.role = UserRole.objects.get(id=request.data['role'])
        user.is_active = False
        user.set_password(request.data['password'])

        user.save()

        user_info = UserInfo.objects.filter(user=user).first()
        if user_info:
            pass
        else:
            user_info = UserInfo.objects.create(
                user=user,
            )

        new_serializer = UserSerializer(user)

        return Response(new_serializer.data, status=status.HTTP_201_CREATED)

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
