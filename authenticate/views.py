from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserRole, User, UserInfo
from .serializers.jwt import CustomTokenObtainPairSerializer
from .serializers.user import UserSerializer, UserDeleteSerializer
from .serializers.user_info import UserInfoSerializer
from .serializers.user_role import UserRoleSerializer
from .services.user import UserCreateService, UserUpdateService


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRoleView(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    create_service = UserCreateService
    update_service = UserUpdateService

    def create(self, request, *args, **kwargs):
        new_user = self.create_service().user_create(request)

        return new_user

    def update(self, request, *args, **kwargs):
        user = self.update_service().user_update(request, *args, **kwargs)

        return user

    @action(["post"], detail=False, permission_classes=[IsAuthenticated], serializer_class=UserDeleteSerializer)
    def delete_request_user(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.is_deleted = True
        user.is_active = False
        user.reason_for_deletion = request.data.get('reason_for_deletion')
        user.save()

        return Response({'message': 'User deleted successfully'})


class UserInfoView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    http_method_names = ['get', 'post', 'put']
    create_service = UserCreateService

    def create(self, request, *args, **kwargs):
        new_user_info = self.create_service().user_info_create(request)

        return new_user_info
