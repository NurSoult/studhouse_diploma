from rest_framework import serializers
from ..models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'photo_avatar', 'contacts', 'email', 'birthDate', 'address', 'imagePaths', 'frontIDCard', 'backIDCard']
