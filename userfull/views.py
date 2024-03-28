from rest_framework import viewsets, permissions
from userfull.models import Student, Landlord
from userfull.serializers.landlord import LandlordSerializer
from userfull.serializers.student import StudentSerializer


class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LandlordView(viewsets.ModelViewSet):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    permission_classes = [permissions.IsAuthenticated]
