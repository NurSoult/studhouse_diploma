from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisement.models import Advertisement, AdvertisementImage
from authenticate.serializers.user import UserSerializer


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

    @staticmethod
    def get_advertisement_images(obj) -> list:
        images = AdvertisementImage.objects.filter(advertisement=obj)
        if images:
            return AdvertisementImageSerializer(images, many=True).data
        return []

    class Meta:
        model = Advertisement
        fields = (
            'id', 'title', 'description', 'price', 'location', 'advertisement_images', 'author', 'creationDate',
            'floor', 'typeOfHouse', 'numberOfRooms', 'square', 'isSold', 'isArchived', 'uploaded_images'
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
