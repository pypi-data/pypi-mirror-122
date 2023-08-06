from django.contrib.auth.models import Permission
from django.db import models
from django_koldar_utils.django_toolbox.Orm import Orm
from django_koldar_utils.django_toolbox.models.AbstractGenericUser import AbstractGenericUser
from django_koldar_utils.django_toolbox.models.mixins.users.DatabaselessPermissionsMixin import DatabaselessPermissionsMixin


class AuthUser(AbstractGenericUser, DatabaselessPermissionsMixin):
    """
    A class that substitute the standard User in django framework. Used to explicitly differentiate with the base user
    class that we are going to use in this django project to store each user additional properties.

    This user is different from the standard one since the permissions are not checked against the database, but rather
    against a cache. Such cache is assumed to be synchronized when authorization (due to authentication) occurs.

    It is important that this table is not managed, since otherwise all the database would have this user
    """
    class Meta:
        db_table = Orm.create_table_name("AuthUser")
        # sadly admin migration requires a User table. Hence we need a "dummy" one
        # TODO managed = False


class AuthUserPermission(models.Model):
    """
    Represents a table specifiying the permissions a user has.
    The user is not stored at all, since the user table is stored in the user-auth-service
    """
    class Meta:
        db_table = Orm.create_table_name("AuthUserPermission")

    id = Orm.primary_id(column_name="id")
    user_id = Orm.required_external_id(
        column_name="user_id",
        description="id of a user. The id are the one from the user authentication service"
    )
    permission = models.ForeignKey(to=Permission, related_name="users", on_delete=models.CASCADE)


class GroupPermission(models.Model):
    """
    Represents a table specifiying the permissions a user has.
    The user is not stored at all, since the user table is stored in the user-auth-service
    """

    class Meta:
        db_table = Orm.create_table_name("GroupPermission")

    id = Orm.primary_id(column_name="id")
    group_id = Orm.required_external_id(
        column_name="group_id",
        description="id of a group. The id are the same one from the user authentication service"
    )
    permission = models.ForeignKey(to=Permission, related_name="groups", on_delete=models.CASCADE)