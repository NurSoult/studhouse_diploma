from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from advertisement.models import Advertisement, AdvertisementFavorite
from advertisement.serializers.advertisement import AdvertisementSerializer, AdvertisementAddFavoriteSerializer, \
    AdvertisementFavoriteSerializer, CreateAdvertisementAddFavoriteSerializer
from authenticate.permissions import IsStudent, IsLandlord


@extend_schema_view(
    list=extend_schema(summary='Get all advertisements', description='Get all advertisements', tags=['advertisement'], responses={200: AdvertisementSerializer(many=True)}),
    retrieve=extend_schema(summary='Get advertisement by id', description='Get advertisement by id', tags=['advertisement']),
    create=extend_schema(summary='Create a new advertisement', description='Create a new advertisement', tags=['advertisement']),
    update=extend_schema(summary='Update advertisement', description='Update advertisement', tags=['advertisement']),
    destroy=extend_schema(summary='Delete advertisement', description='Delete advertisement', tags=['advertisement']),
    get_favorite_advertisements=extend_schema(summary='Get favorite advertisements', description='Get favorite advertisements', tags=['advertisement'], responses={200: AdvertisementFavoriteSerializer(many=True)}),
    add_to_favorite=extend_schema(summary='Add advertisement to favorite', description='Add advertisement to favorite', tags=['advertisement'], responses={200: OpenApiResponse(description='Advertisement added to favorites')}, request=CreateAdvertisementAddFavoriteSerializer),
    get_my_advertisements=extend_schema(summary='Get my advertisements', description='Get my advertisements', tags=['advertisement'], responses={200: AdvertisementSerializer(many=True)}),
)
class AdvertisementView(viewsets.ModelViewSet):
    queryset = Advertisement.objects.order_by('-creationDate')
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        author = request.user.id
        if IsLandlord().has_permission(request, self):
            request.data['author'] = author
        else:
            return Response({"message": "Only landlords can create advertisements."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(["get"], detail=False, permission_classes=[permissions.IsAuthenticated], serializer_class=AdvertisementSerializer)
    def get_favorite_advertisements(self, request, *args, **kwargs) -> Response:
        favorite_advertisements = AdvertisementFavorite.objects.filter(user=request.user)
        data = [advertisement.advertisement for advertisement in favorite_advertisements]
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post"], detail=False, permission_classes=[permissions.IsAuthenticated], serializer_class=AdvertisementAddFavoriteSerializer)
    def add_to_favorite(self, request, *args, **kwargs):
        try:
            advertisement = Advertisement.objects.get(id=request.data['advertisement'])
        except Advertisement.DoesNotExist:
            return Response({"message": "Advertisement not found."}, status=status.HTTP_400_BAD_REQUEST)

        if AdvertisementFavorite.objects.filter(advertisement=advertisement, user=request.user).exists():
            return Response({"message": "Advertisement already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        AdvertisementFavorite.objects.create(advertisement=advertisement, user=request.user)

        return Response({"message": "Advertisement added to favorites."}, status=status.HTTP_200_OK)

    @action(["get"], detail=False, permission_classes=[permissions.IsAuthenticated], serializer_class=AdvertisementSerializer)
    def get_my_advertisements(self, request, *args, **kwargs) -> Response:
        my_advertisements = Advertisement.objects.filter(author=request.user)
        response = [AdvertisementSerializer(advertisement).data for advertisement in my_advertisements]
        return Response(response, status=status.HTTP_200_OK)
