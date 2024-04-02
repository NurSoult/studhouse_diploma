from rest_framework import serializers
from .user_info import UserInfoSerializer
from .user_role import UserRoleSerializer
from ..models import User, AdditionalUser


class AdditionalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalUser
        fields = ['full_name', 'who_is', 'contacts']


class UserSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(read_only=True)
    user_info = UserInfoSerializer(read_only=True)
    additional_user = AdditionalUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'login', 'full_name', 'is_active', 'is_deleted', 'role', 'user_info', 'additional_user']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'role', 'login', 'full_name', 'password', 'is_active', 'is_staff', 'is_superuser']


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    contacts = serializers.CharField(required=False)
    photo_avatar = serializers.ImageField(required=False)
    birthDate = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    imagePaths = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = User
        fields = ['id', 'role', 'login', 'full_name', 'email', 'contacts', 'photo_avatar', 'is_active', 'is_deleted', 'birthDate', 'address', 'imagePaths']


class UserDeleteSerializer(serializers.ModelSerializer):
    reason_for_deletion = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'reason_for_deletion']


class AddAdditionalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalUser
        fields = ['user', 'full_name', 'who_is', 'contacts']


class UserActivateSerializer(serializers.ModelSerializer):
    login = serializers.EmailField()
    code = serializers.CharField()

    class Meta:
        model = User
        fields = ['login', 'code']


class UserSendActivationCodeSerializer(serializers.ModelSerializer):
    login = serializers.EmailField()

    class Meta:
        model = User
        fields = ['login']


class UserSendResetPasswordCodeSerializer(serializers.ModelSerializer):
    login = serializers.EmailField()

    class Meta:
        model = User
        fields = ['login']


class UserCheckResetCodeSerializer(serializers.ModelSerializer):
    login = serializers.EmailField()
    code = serializers.CharField()

    class Meta:
        model = User
        fields = ['login', 'code']


class UserResetPasswordSerializer(serializers.ModelSerializer):
    login = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['login', 'password']
