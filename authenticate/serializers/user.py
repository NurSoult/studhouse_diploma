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
        fields = ['id', 'role', 'login', 'full_name']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'login', 'full_name']


class UserDeleteSerializer(serializers.ModelSerializer):
    reason_for_deletion = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'reason_for_deletion']
