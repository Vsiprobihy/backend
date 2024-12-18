from rest_framework.permissions import BasePermission

from .models import CustomUser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.ADMIN and request.user.is_superuser


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == CustomUser.ORGANIZER
        )
