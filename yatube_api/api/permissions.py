from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return obj.author == request.user

    def has_obj_permission(self, request, view, obj):
        if obj.author != request.user:
            return obj.author == request.user
