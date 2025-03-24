from rest_framework.permissions import BasePermission

class AccessToGamePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in (obj.user1,obj.user2)
