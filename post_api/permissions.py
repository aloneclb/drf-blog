from rest_framework import permissions



class IsAdminUserOrReadOnly(permissions.BasePermission):
    # Admin doğrulaması
    def has_permission(self, request, view):
        is_admin = request.user and request.user.is_staff
        sonuc = request.method in permissions.SAFE_METHODS or is_admin
        return sonuc 


class IsOwnerOrReadOnly(permissions.BasePermission):
    # Post sahibi doğrulaması
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


        return obj.author == request.user