from rest_framework.permissions import BasePermission


class AuthorOrStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().author