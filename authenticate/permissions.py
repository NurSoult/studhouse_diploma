from rest_framework import permissions
from userfull.models import Student, Landlord


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            student = Student.objects.get(user=request.user)
            return True
        except Student.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            student = Student.objects.get(user=request.user)
            return True
        except Student.DoesNotExist:
            return False


class IsLandlord(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            landlord = Landlord.objects.get(user=request.user)
            return True
        except Landlord.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            landlord = Landlord.objects.get(user=request.user)
            return True
        except Landlord.DoesNotExist:
            return False
