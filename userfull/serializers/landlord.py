from rest_framework import serializers
from userfull.models import Landlord


class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = ('id', 'user', 'photo_avatar', 'contacts', 'email', 'birthDate', 'address', 'imagePaths')
