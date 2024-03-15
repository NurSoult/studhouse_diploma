from rest_framework import serializers
from ..models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    photo_avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ['user', 'photo_avatar', 'contacts', 'email', 'is_deleted']
