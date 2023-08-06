from typing import List, Set

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache.backends.locmem import LocMemCache
from django_koldar_utils.django_toolbox import django_helpers
from django_koldar_utils.django_toolbox.models.AbstractGenericUser import AbstractGenericUser

from django_cbim_general_service.models import AuthUser

import logging

LOG = logging.getLogger(__name__)


class UserCache(LocMemCache):
    """
    An extension of mem cache that provides just additional methods.
    he users are indexed by their token.

    This cache contains the tables "users" and "roles".
    """

    def update_user(self, user: AuthUser, roles: List[str], user_permissions: List[Permission], group_permissions: List[Permission], token: str):
        """
        Update the cache by adding 2 links: one between primary key and user information and the other between
        token and user information

        :param user: user to cache
        :param roles: roles assopciated with the user
        :param user_permissions: permissions associated with the user
        :param group_permissions: permissions associated with all the groups
        :param token: token to link
        :return: cached user
        """
        data = dict(user=user, roles=list(roles), user_permissions=user_permissions, group_permissions=group_permissions)
        # we index data by both the token and the user primary key
        self.get_or_set(token, data)
        self.get_or_set(django_helpers.get_primary_key_value(user), data)

    def update_user_indexed_primary_key(self, user: AuthUser, roles: List[str], user_permissions: List[Permission], group_permissions: List[Permission]):
        """
        Update the cache by adding a link between primary key and user information

        :param user: user to cache
        :param roles: roles assopciated with the user
        :param user_permissions: permissions associated with the user
        :param group_permissions: permissions associated with all the groups
        :return: cache user
        """
        data = dict(user=user, roles=list(roles), user_permissions=user_permissions, group_permissions=group_permissions)
        self.get_or_set(django_helpers.get_primary_key_value(user), data)

    def update_user_indexed_token(self, user: AuthUser, token: str):
        """
        Update the cache by updating the link between token and user. Failes if the user is not already cached
        with its primary key as well
        :param user: user to update
        :param token: token to link with the given user
        :return: cached user
        """
        cached_user = self.get(django_helpers.get_primary_key_value(user))
        if cached_user is None:
            LOG.error(f"user {user} not found!")
            raise KeyError(f"There is no user saved in the server")
        return self.get_or_set(token, cached_user)

    def get_user_by_id(self, user_primary_key) -> AuthUser:
        """
        get the user using the primary key
        :param user_primary_key: primary key
        :return:
        """
        user = self.get(user_primary_key)
        if user is None:
            raise ValueError(f"key {user_primary_key} is not prsent in the user cache.")
        return user["user"]

    def get_user_permissions(self, user_id: int) -> Set[Permission]:
        result = self.get(user_id)
        if result is None:
            return set()
        return set(result["user_permissions"])

    def get_group_permissions(self, user_id: int) -> Set[Permission]:
        result = self.get(user_id)
        if result is None:
            return set()
        return set(result["group_permissions"])
