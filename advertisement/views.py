from rest_framework import viewsets, permissions

from advertisement.models import Advertisement
from advertisement.serializers.advertisement import AdvertisementSerializer


class AdvertisementView(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
