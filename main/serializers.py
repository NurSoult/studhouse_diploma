from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from authenticate.serializers.user import UserSerializer
from .models import Review, RelocationImage, Relocation, RelocationFavorite


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RelocationOwnerSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=50)


class RelocationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelocationImage
        fields = ['image']
        kwargs = {
            'image': {
                'write_only': True,
                'required': False,
                'allow_null': True,
                'allow_empty_file': True,
            }
        }


class RelocationSerializer(serializers.ModelSerializer):
    relocation_images = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=True, use_url=False, allow_null=True),
        write_only=True,
        required=False
    )
    creationDate = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    owner = serializers.SerializerMethodField()
    price = serializers.IntegerField()
    is_favorite = serializers.SerializerMethodField()

    @staticmethod
    def get_relocation_images(obj) -> list:
        images = RelocationImage.objects.filter(relocation=obj)
        if images:
            return RelocationImageSerializer(images, many=True).data
        return []

    @staticmethod
    def get_owner(obj) -> dict:
        return RelocationOwnerSerializer({
            'full_name': obj.author.full_name,
            'phone_number': obj.author.user_info.contacts
        }).data

    def get_is_favorite(self, obj) -> bool:
        return RelocationFavorite.objects.filter(relocation=obj, user=self.context['request'].user).exists()

    class Meta:
        model = Relocation
        fields = (
            'id', 'title', 'author', 'description', 'price', 'location', 'relocation_images', 'paymentTime', 'owner', 'creationDate', 'floor', 'typeOfHouse', 'max_people_count', 'current_people_count', 'count_bedrooms', 'count_bathrooms', 'numberOfRooms', 'square', 'isSold', 'isArchived', 'haveWifi', 'haveTV', 'haveWashingMachine',
            'haveParking', 'haveConditioner', 'nearbyTradeCenter', 'nearbyHospital', 'nearbySchool', 'nearbyGym', 'university', 'course', 'profession', 'is_favorite', 'uploaded_images'
        )

    def create(self, validated_data):
        """ uploaded_images not required """

        if 'uploaded_images' not in validated_data:
            return Relocation.objects.create(**validated_data)

        uploaded_images = validated_data.pop('uploaded_images', None)
        relocation = Relocation.objects.create(**validated_data)

        relocation_images = [
            RelocationImage(relocation=relocation, image=image) for image in uploaded_images
        ]

        for image in relocation_images:
            image.full_clean()

        try:
            with transaction.atomic():
                RelocationImage.objects.bulk_create(relocation_images)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return relocation


class RelocationFavoriteSerializer(serializers.ModelSerializer):
    relocation = RelocationSerializer(read_only=True)

    class Meta:
        model = RelocationFavorite
        fields = ["relocation"]


class RelocationAddFavoriteSerializer(serializers.ModelSerializer):
    relocation = RelocationSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = RelocationFavorite
        fields = ["relocation", "user"]


class CreateRelocationAddFavoriteSerializer(serializers.Serializer):
    relocation = serializers.IntegerField()


class ReportSerializer(serializers.Serializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    text = serializers.CharField(max_length=500)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
