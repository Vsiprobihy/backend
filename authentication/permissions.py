from rest_framework.permissions import BasePermission
from .models import CustomUser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.ADMIN


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.ORGANIZER
