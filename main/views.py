from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializers import ReviewSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all reviews', description='Get all reviews', tags=['review'], responses={200: ReviewSerializer(many=True)}),
    create=extend_schema(summary='Create a new review', description='Create a new review', tags=['review']),
)
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post']
