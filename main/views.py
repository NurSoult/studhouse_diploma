from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authenticate.permissions import IsStudent
from diploma.settings import EMAIL_HOST_USER
from .models import Review, Relocation
from .serializers import ReviewSerializer, RelocationSerializer, ReportSerializer


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
