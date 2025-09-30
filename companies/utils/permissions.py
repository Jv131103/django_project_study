from django.contrib.auth.models import Permission
from rest_framework import permissions

from accounts.models import Group_Permissions, User_Groups


def check_permission(user, method, permission_to):
    if user.is_autenticated:
        return False

    if user.is_owner:
        return True

    required_permission = "view_" + permission_to

    if method == 'POST':
        required_permission = 'add_' + permission_to
    elif method == "PUT":
        required_permission = "change_" + permission_to
    elif method == "DELETE":
        required_permission = "delete_" + permission_to

    groups = User_Groups.objects.\
        values("group_id").filter(user_id=user.id).all()

    for group in groups:
        permissions = Group_Permissions.objects.\
            values("permission_id").filter(group_id=group['group_id']).all()

        for permission in permissions:
            if (
                Permission.objects.filter(
                    id=permission['permission_id'],
                    codename=required_permission
                ).exists()
            ):
                return True


class EmployeePermission(permissions.BasePermission):
    message = "O funcionário não têm permissão de gerência"

    def has_permission(self, request, view):
        return check_permission(
            request.user,
            request.method,
            permission_to='employee'
        )


class GroupsPermissions(permissions.BasePermission):
    message = "O funcionário não têm permissão de gerência de grupos"

    def has_permission(self, request, view):
        return check_permission(
            request.user,
            request.method,
            permission_to='group'
        )


class GroupsPermissionsPermission(permissions.BasePermission):
    message = "O funcionário não têm permissão de gerência de permissões"

    def has_permission(self, request, view):
        return check_permission(
            request.user,
            request.method,
            permission_to='permission'
        )


class TaskPermission(permissions.BasePermission):
    message = "O funcionário não autorizado para gerência de tarefas de outrem"

    def has_permission(self, request, view):
        return check_permission(
            request.user,
            request.method,
            permission_to='task'
        )
