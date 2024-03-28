from rest_framework import serializers

from authenticate.serializers.user import UserSerializer
from userfull.models import Landlord


class LandlordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Landlord
        fields = ('id', 'name', 'email', 'phone', 'user')
