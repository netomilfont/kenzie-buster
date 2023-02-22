from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User

class IsEmployeeOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated 
            and request.user.is_superuser
        )

class IsNotYourAccount(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):

        if not request.user.is_authenticated:
            return False
        
        if request.user.is_employee == False and request.user.id == obj.id:
            return True

        return (
            request.user.id == obj.id or request.user.is_employee
        )