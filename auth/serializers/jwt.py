from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from diploma.auth.exceptions import UserNotActive, UserNotFound, UserCredentialsError
from diploma.auth.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login, password = attrs['login'], attrs['password']

        user = User.objects.filter(login=login).first()

        if user is not None:
            if not user.is_active:
                raise UserNotActive

            try:
                return super().validate(attrs)
            except AuthenticationFailed:
                raise UserCredentialsError
        else:
            raise UserNotFound
