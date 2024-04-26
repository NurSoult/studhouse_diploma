from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authenticate.permissions import IsStudent
from .models import Review, Relocation
from .serializers import ReviewSerializer, RelocationSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all reviews', description='Get all reviews', tags=['review'], responses={200: ReviewSerializer(many=True)}),
    create=extend_schema(summary='Create a new review', description='Create a new review', tags=['review']),
)
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post']


class RelocationViewSet(ModelViewSet):
    queryset = Relocation.objects.all()
    serializer_class = RelocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        author = request.user.id
        if IsStudent().has_permission(request, self):
            request.data['author'] = author
        else:
            return Response({"message": "Only students can create relocations."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
