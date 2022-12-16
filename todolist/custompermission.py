from rest_framework import permissions

class IsOwnwerPermission(permissions.BasePermission):
    message="you have no permission"
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user