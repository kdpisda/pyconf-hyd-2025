from rest_framework import permissions


class TodoPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Block DELETE operations for everyone
        if request.method == "DELETE":
            return False

        # Staff can view everything
        if request.user.is_staff:
            return True

        # Regular users can only see their own items
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        # For Item model, check the list owner
        return obj.list.owner == request.user
