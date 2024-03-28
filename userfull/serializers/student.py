from rest_framework import serializers
from userfull.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'user', 'photo_avatar', 'contacts', 'email', 'birthDate', 'address', 'imagePaths')
