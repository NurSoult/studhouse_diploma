from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authenticate.permissions import IsStudent
from diploma.settings import EMAIL_HOST_USER
from .models import Review, Relocation, RelocationFavorite
from .serializers import ReviewSerializer, RelocationSerializer, ReportSerializer, RelocationAddFavoriteSerializer, \
    RelocationFavoriteSerializer, CreateRelocationAddFavoriteSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all reviews', description='Get all reviews', tags=['review'], responses={200: ReviewSerializer(many=True)}),
    create=extend_schema(summary='Create a new review', description='Create a new review', tags=['review']),
)
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post']


@extend_schema_view(
    list=extend_schema(summary='Get all relocations', description='Get all relocations', tags=['relocation'], responses={200: RelocationSerializer(many=True)}),
    create=extend_schema(summary='Create a new relocation', description='Create a new relocation', tags=['relocation'], responses={201: RelocationSerializer}),
    update=extend_schema(summary='Update a relocation', description='Update a relocation', tags=['relocation'], responses={200: RelocationSerializer}),
    partial_update=extend_schema(summary='Partially update a relocation', description='Partially update a relocation', tags=['relocation'], responses={200: RelocationSerializer}),
    destroy=extend_schema(summary='Delete a relocation', description='Delete a relocation', tags=['relocation'], responses={204: None}),
    get_favorite_relocations=extend_schema(summary='Get favorite relocations', description='Get favorite relocations', tags=['relocation'], responses={200: RelocationFavoriteSerializer(many=True)}),
    add_to_favorite=extend_schema(summary='Add relocation to favorite', description='Add relocation to favorite', tags=['relocation'], responses={200: OpenApiResponse(description='Relocation added to favorites')}, request=CreateRelocationAddFavoriteSerializer),
    get_my_relocations=extend_schema(summary='Get my relocations', description='Get my relocations', tags=['relocation'], responses={200: RelocationSerializer(many=True)})
)
class RelocationViewSet(ModelViewSet):
    queryset = Relocation.objects.order_by('-creationDate')
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

    @action(["get"], detail=False, permission_classes=[permissions.IsAuthenticated],
            serializer_class=RelocationSerializer)
    def get_favorite_relocations(self, request, *args, **kwargs) -> Response:
        favorite_relocations = RelocationFavorite.objects.filter(user=request.user)
        data = [advertisement.relocation for advertisement in favorite_relocations]
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post"], detail=False, permission_classes=[permissions.IsAuthenticated],
            serializer_class=RelocationAddFavoriteSerializer)
    def add_to_favorite(self, request, *args, **kwargs):
        try:
            relocation = Relocation.objects.get(id=request.data['relocation'])
        except Relocation.DoesNotExist:
            return Response({"message": "Relocation not found."}, status=status.HTTP_400_BAD_REQUEST)

        if RelocationFavorite.objects.filter(relocation=relocation, user=request.user).exists():
            return Response({"message": "Relocation already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        RelocationFavorite.objects.create(relocation=relocation, user=request.user)

        return Response({"message": "Relocation added to favorites."}, status=status.HTTP_200_OK)

    @action(["get"], detail=False, permission_classes=[permissions.IsAuthenticated], serializer_class=RelocationSerializer)
    def get_my_relocations(self, request, *args, **kwargs) -> Response:
        my_relocations = Relocation.objects.filter(author=request.user)
        serializer = self.get_serializer(my_relocations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    create=extend_schema(summary='Create a new report', description='Create a new report', tags=['report'], responses={201: ReportSerializer}),
)
class ReportView(ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        author = request.user
        request.data['author'] = author

        text = request.data['text']
        date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Report'
        message = f'''
            Report created by user: {author.login}.
            Date: {date}.
            Text: {text}.
            
            Please, check the report.
        '''

        try:
            with transaction.atomic():
                send_mail(
                    subject,
                    message,
                    EMAIL_HOST_USER,
                    ['studhouse.rep@gmail.com']
                )

                send_mail(
                    subject,
                    f'You sent a report to the administration. Date: {date}. Text: {text}.',
                    EMAIL_HOST_USER,
                    [author.login]
                )

                return Response({"message": "Report sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
