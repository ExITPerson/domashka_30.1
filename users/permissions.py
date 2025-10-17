from rest_framework import permissions


class ModeratorsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.groups.filter(name='Moderators').exists():
            return True
        else:
            return False