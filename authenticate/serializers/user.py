from rest_framework import serializers
from .user_info import UserInfoSerializer
from .user_role import UserRoleSerializer
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    user_info = UserInfoSerializer(read_only=True)

    @staticmethod
    def get_role(obj):
        return UserRoleSerializer(obj.role).data

    class Meta:
        model = User
        fields = ['id', 'login', 'full_name', 'is_active', 'is_deleted', 'role', 'user_info']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'role', 'login', 'full_name', 'password']


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
