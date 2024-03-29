from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from advertisement.models import Advertisement, AdvertisementFavorite
from advertisement.serializers.advertisement import AdvertisementSerializer, AdvertisementAddFavoriteSerializer, \
    AdvertisementFavoriteSerializer


class AdvertisementView(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("request_user:", request.user.id)
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)

    @action(["get"], detail=False, permission_classes=[permissions.IsAuthenticated], serializer_class=AdvertisementFavoriteSerializer)
    def get_favorite_advertisements(self, request, *args, **kwargs) -> Response:
        favorite_advertisements = AdvertisementFavorite.objects.filter(user=request.user)
        response = [AdvertisementSerializer(favorite.advertisement).data for favorite in favorite_advertisements]
        return Response(response, status=status.HTTP_200_OK)

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
