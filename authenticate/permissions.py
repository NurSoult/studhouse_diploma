from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role.role_name == 'Student':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role.role_name == 'Student':
            return True
        else:
            return False


class IsLandlord(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role.role_name == 'Landlord':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role.role_name == 'Landlord':
            return True
        else:
            return False
