from rest_framework import serializers
from advertisement.models import Advertisement
from authenticate.serializers.user import UserSerializer


class AdvertisementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = (
            'id', 'title', 'description', 'price', 'location', 'imagePaths', 'author', 'creationDate',
            'floor', 'typeOfHouse', 'numberOfRooms', 'square', 'isSold', 'isArchived'
        )
