from rest_framework import serializers

from authenticate.serializers.user import UserSerializer
from userfull.models import Student


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'phone', 'user')
