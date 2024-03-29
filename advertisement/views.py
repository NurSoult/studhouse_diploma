from rest_framework import viewsets, permissions

from advertisement.models import Advertisement
from advertisement.serializers.advertisement import AdvertisementSerializer


class AdvertisementView(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("request_user:", request.user.id)
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)
