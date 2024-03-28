from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserRole, User, UserInfo
from .serializers.jwt import CustomTokenObtainPairSerializer
from .serializers.user import UserSerializer, UserDeleteSerializer, UserCreateSerializer, UserUpdateSerializer
from .serializers.user_info import UserInfoSerializer
from .serializers.user_role import UserRoleSerializer
from .services.user import UserCreateService, UserUpdateService


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all user roles', description='Get all user roles', tags=['user role'], responses={200: UserRoleSerializer(many=True)}),
    retrieve=extend_schema(summary='Get user role by id', description='Get user role by id', tags=['user role']),
    create=extend_schema(summary='Create a new user role', description='Create a new user role', tags=['user role']),
    update=extend_schema(summary='Update user role', description='Update user role', tags=['user role']),
    destroy=extend_schema(summary='Delete user role', description='Delete user role', tags=['user role'])
)
class UserRoleView(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


@extend_schema_view(
    list=extend_schema(summary='Get all users', description='Get all users', tags=['user'], responses={200: UserSerializer(many=True)}),
    retrieve=extend_schema(summary='Get user by id', description='Get user by id', tags=['user']),
    create=extend_schema(summary='Create a new user', description='Create a new user', tags=['user']),
    partial_update=extend_schema(summary='Update user', description='Update user', tags=['user']),
    destroy=extend_schema(summary='Delete user', description='Delete user', tags=['user']),
    delete_request_user=extend_schema(summary='Delete request user', description='Delete request user', tags=['user'])
)
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    create_service = UserCreateService
    update_service = UserUpdateService

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'partial_update':
            return UserUpdateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        new_user = self.create_service().user_create(request)

        return new_user

    def partial_update(self, request, *args, **kwargs):
        user = self.update_service().user_update(request, *args, **kwargs)

        return user

    @action(["get"], detail=False, permission_classes=[IsAuthenticated], serializer_class=UserSerializer)
    def get_request_user(self, request, *args, **kwargs):
        print("request_user:", request.user)
        user = User.objects.get(id=request.user.id)
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data)

    @action(["post"], detail=False, permission_classes=[IsAuthenticated], serializer_class=UserDeleteSerializer)
    def delete_request_user(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.is_deleted = True
        user.is_active = False
        user.reason_for_deletion = request.data.get('reason_for_deletion')
        user.save()

        return Response({'message': 'User deleted successfully'})


@extend_schema_view(
    list=extend_schema(summary='Get all user info', description='Get all user info', tags=['user info'], responses={200: UserInfoSerializer(many=True)}),
    retrieve=extend_schema(summary='Get user info by id', description='Get user info by id', tags=['user info']),
    create=extend_schema(summary='Create a new user info', description='Create a new user info', tags=['user info']),
    update=extend_schema(summary='Update user info', description='Update user info', tags=['user info']),
    destroy=extend_schema(summary='Delete user info', description='Delete user info', tags=['user info'])
)
class UserInfoView(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    http_method_names = ['get', 'post', 'put']
    create_service = UserCreateService

    def create(self, request, *args, **kwargs):
        new_user_info = self.create_service().user_info_create(request)

        return new_user_info
