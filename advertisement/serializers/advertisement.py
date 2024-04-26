from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisement.models import Advertisement, AdvertisementImage, AdvertisementFavorite
from authenticate.serializers.user import UserSerializer


class AdvertisementOwnerSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=50)


class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['image']
        kwargs = {
            'image': {
                'write_only': True,
                'required': False,
                'allow_null': True,
                'allow_empty_file': True,
            }
        }


class AdvertisementSerializer(serializers.ModelSerializer):
    advertisement_images = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=True, use_url=False, allow_null=True),
        write_only=True,
        required=False
    )
    creationDate = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    owner = serializers.SerializerMethodField()
    price = serializers.IntegerField()

    @staticmethod
    def get_advertisement_images(obj) -> list:
        images = AdvertisementImage.objects.filter(advertisement=obj)
        if images:
            return AdvertisementImageSerializer(images, many=True).data
        return []

    @staticmethod
    def get_owner(obj) -> dict:
        return AdvertisementOwnerSerializer({
            'full_name': obj.author.full_name,
            'phone_number': obj.author.user_info.contacts
        }).data

    class Meta:
        model = Advertisement
        fields = (
            'id', 'title', 'author', 'description', 'price', 'location', 'advertisement_images', 'paymentTime', 'owner', 'creationDate',
            'floor', 'typeOfHouse', 'count_bedrooms', 'count_bathrooms', 'numberOfRooms', 'square', 'isSold', 'isArchived', 'haveWifi', 'haveTV', 'haveWashingMachine',
            'haveParking', 'haveConditioner', 'nearbyTradeCenter', 'nearbyHospital', 'nearbySchool', 'nearbyGym', 'uploaded_images'
        )

    def create(self, validated_data):
        """ uploaded_images not required """

        if 'uploaded_images' not in validated_data:
            return Advertisement.objects.create(**validated_data)

        uploaded_images = validated_data.pop('uploaded_images', None)
        advertisement = Advertisement.objects.create(**validated_data)

        advertisement_images = [
            AdvertisementImage(advertisement=advertisement, image=image) for image in uploaded_images
        ]

        for image in advertisement_images:
            image.full_clean()

        try:
            with transaction.atomic():
                AdvertisementImage.objects.bulk_create(advertisement_images)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return advertisement


class AdvertisementFavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = AdvertisementFavorite
        fields = ["advertisement"]


class AdvertisementAddFavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdvertisementFavorite
        fields = ["advertisement", "user"]


class CreateAdvertisementAddFavoriteSerializer(serializers.Serializer):
    advertisement = serializers.IntegerField()
