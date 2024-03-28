from rest_framework import serializers
from advertisement.models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = (
            'id', 'title', 'description', 'price', 'location', 'imagePaths', 'author', 'creationDate',
            'floor', 'typeOfHouse', 'numberOfRooms', 'square', 'isSold', 'isArchived'
        )
