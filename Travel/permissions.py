from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.author:
            return True
        return False

class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.user == obj.user :
            return True
        return False