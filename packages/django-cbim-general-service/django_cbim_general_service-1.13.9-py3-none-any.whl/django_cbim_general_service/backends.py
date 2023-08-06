import functools
from calendar import timegm
from datetime import datetime
from typing import Optional, List, Set, Dict

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission
from django.core.cache import caches
from django.http import HttpRequest
from django_graphene_authentication.backend import AbstractStandardAuthenticateViaApiTokenAuthenticationBackend, \
    AbstractAuthenticateViaAccessToken
from django_graphene_authentication.decorators import csrf_rotation
from django.utils.translation import gettext as _
from graphene.utils.thenables import maybe_thenable
from graphql_jwt import exceptions, signals
from graphql_jwt.decorators import setup_jwt_cookie, on_token_auth_resolve
from graphql_jwt.settings import jwt_settings

from django_cbim_general_service.conf import settings

from django_cbim_general_service.cache import UserCache
from django_cbim_general_service.models import AuthUser, GroupPermission, AuthUserPermission


class AbstractGeneralServiceAuthenticateViaAccessTokenAuthenticationBackend(AbstractAuthenticateViaAccessToken):
    """
    This authentication backend allows you to authenticate if you have a access_token. If you have it (either
    from a graphql argument or inside a HTTP authorization field) you can use this authentication method. This method
    will update a "user" cache with information regarding user, group and permissions.
    """

    def do_after_user_authenticated(self, request: HttpRequest, authenticating_token: str, user: any, payload: any,
                                    **kwargs):
        pass

    def enable_backend(self, request, token, **kwargs) -> bool:
        """
        The backend is run only if "are_we_authenticating_from_login_mutation" is present in the rquest
        """
        if not super().enable_backend(request, token, **kwargs):
            return False
        if not getattr(request, 'are_we_authenticating_from_login_mutation', False):
            # we want to authenticate ONLY if we are inside the authentication mutation. Otherwise, this backend needs to be disabled
            # (since access_token shoud be processed only in login mutation)
            return False
        return True

    def jwt_token_secret_key(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["ACCESS_TOKEN_SECRET_KEY"]

    def jwt_token_public_key(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["ACCESS_TOKEN_PUBLIC_KEY"]

    def jwt_token_audience(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["ACCESS_TOKEN_AUDIENCE"]

    def jwt_token_issuer(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["ACCESS_TOKEN_ISSUER"]

    def jwt_token_algorithm(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["ACCESS_TOKEN_ALGORITHM"]

    def jwt_token_name(self) -> str:
        return "access_token"

    def get_user_permissions(self, user_obj: AuthUser, obj=None) -> Set[Permission]:
        # we have populate the cache during authentication. We just fetch permissions
        cache: UserCache = caches[self._get_cache_name()]
        return cache.get_user_permissions(user_id=user_obj.id)

    def get_group_permissions(self, user_obj: AuthUser, obj=None) -> Set[Permission]:
        cache: UserCache = caches[self._get_cache_name()]
        return cache.get_group_permissions(user_id=user_obj.id)

    def _get_user_by_payload(self, payload: any, request: HttpRequest, **kwargs) -> any:
        """
        fetch the user from the access token, then update the cache
        """
        username = payload["username"]
        user_id = payload["sub"]
        roles = payload["roles"]

        # fetch user permissions
        user_permissions = self._get_user_permissions(user_id)
        group_permissions = set()
        for r in roles:
            group_permissions = group_permissions.union(self._get_role_permissions(role_id=r["id"], role_name=r["name"]))
        user = self._save_user_info_in_cache(
            user_id=user_id,
            username=username,
            roles=roles,
            user_permissions=user_permissions,
            group_permissions=group_permissions
        )

        return user

    def _get_user_permissions(self, user_id: int) -> List[Permission]:
        """
        Fetches the permissions attached to the user
        :param user_id: id of the user whose permissions we need to fetch
        :return: list of permissions. Each permission has an id and a name
        """
        return [up.permission for up in AuthUserPermission.objects.filter(user_id=user_id)]

    def _get_role_permissions(self, role_id: int, role_name: str) -> List[Permission]:
        return [up.permission for up in GroupPermission.objects.filter(group_id=role_id)]

    def _get_cache_name(self) -> str:
        """
        Returns the cache name that we are going to use to store permissions
        :return: name fo the cache to use
        """

        return "users"

    def _save_user_info_in_cache(self, user_id: int, username: str, roles: List[Dict[str, any]],
                                user_permissions: List[Permission], group_permissions: Set[Permission]) -> AuthUser:
        """
        Overrideable. Save the user to the database or in another place.
        We first fetch the information of user_permissions and roles_permissions. Then we add them all in
        the user cache.

        :param user_id: id of the user to save. Comes from the authentication service
        :param username: username of the user to save. Comes from the authentication service
        :param roles: roles of the user to save. dictionaries of id (int) and name (str)
        :param user_permissions: lits of permissions associated to the user
        :param group_permissions: list of permissions associated to every group containing the user
        :param token: access token
        :return: user object. Information about the user has been successfully updated
        """
        cache: UserCache = caches[self._get_cache_name()]
        user = AuthUser(
            id=user_id,
            username=username
        )
        # fetch all the user_roles and user_permissions
        cache.update_user_indexed_primary_key(user, roles, user_permissions, group_permissions)
        return user


class AbstractGeneralServiceAuthenticateViaApiTokenAuthenticationBackend(AbstractStandardAuthenticateViaApiTokenAuthenticationBackend):
    """
    This authentication backend allows you to authenticate if you have a api_token. If you have it (either
    from a graphql argument or inside a HTTP authorization field) you can use this authentication method.
    This method will update the user cache with this api_token: in this way you can search a user by inputting
    the api_token.
    """

    def do_after_user_authenticated(self, request: HttpRequest, authenticating_token: str, user: any, payload: any,
                                    **kwargs):
        # update cache with the api_token
        user_cache: UserCache = caches[self._get_cache_name()]
        user_cache.update_user_indexed_token(user, authenticating_token)

    def jwt_token_secret_key(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_SECRET_KEY"]

    def jwt_token_public_key(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_PUBLIC_KEY"]

    def jwt_token_name(self) -> str:
        return "api_token"

    def _get_user_by_payload(self, payload: any, request: HttpRequest, **kwargs) -> any:
        """
        fetch the user from the api token, then update the cache
        """
        user_id = payload["sub"]

        user_cache: UserCache = caches[self._get_cache_name()]
        user = user_cache.get_user_by_id(user_id)

        return user

    def _get_cache_name(self) -> str:
        """
        Returns the cache name that we are going to use to store permissions
        :return: name fo the cache to use
        """

        return "users"


# import functools
# import logging
# from calendar import timegm
# from datetime import datetime
#
# from typing import Dict, Set, Optional, List
#
# from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.backends import BaseBackend, ModelBackend
# from django.contrib.auth.models import User, Permission
# from django.core.cache import caches
#
#
# from django_koldar_utils.django.AbstactBackend import AbstractDjangoBackend, TPERMISSION, TUSER, TUSER_ID
# from django_koldar_utils.django.models.AbstractGenericUser import AbstractGenericUser
# from django_koldar_utils.functions import decorators
# from graphql_jwt import utils as graphql_jwt_utils
# from graphql_jwt.backends import JSONWebTokenBackend
# from graphql_jwt.decorators import setup_jwt_cookie, csrf_rotation, refresh_expiration, on_token_auth_resolve
# from graphene.utils.thenables import maybe_thenable
# from graphql_jwt import signals
# from graphql_jwt.settings import jwt_settings
#
# from django_cbim_general_service.cache import UserCache
# from django_cbim_general_service.models import AuthUser
#
# from graphql_jwt import utils as graphjwt_utils, exceptions
# from django.utils.translation import gettext as _
#
# LOG = logging.getLogger(__name__)
#
#
# class GeneralServiceAuthenticationViaAccessTokenBackend(AbstractDjangoBackend[AuthUser, int, Permission]):
#     """
#     Assumes there is a access token. We decode it and generate the api_token
#     """
#
#     def authenticate(self, request, **kwargs) -> Optional[TUSER]:
#         pass
#
#     def get_user(self, user_id: TUSER_ID) -> Optional[TUSER]:
#         return
#
#     @property
#     def cache_name(self) -> str:
#         return "users"
#
#     def get_user_permissions(self, user_obj: AuthUser, obj=None) -> Set[TPERMISSION]:
#         # we have populate the cache during authentication. We just fetch permissions
#         cache: UserCache = caches[self.cache_name]
#         return cache.get_user_permissions(user_id=user_obj.id)
#
#     def get_group_permissions(self, user_obj: AuthUser, obj=None) -> Set[TPERMISSION]:
#         cache: UserCache = caches[self.cache_name]
#         return cache.get_group_permissions(user_id=user_obj.id)
#
#
# class GeneralServiceAuthenticationBackend(AbstractDjangoBackend[AuthUser, int, Permission], JSONWebTokenBackend):
#     """
#     We have decided that in our architecture, users and roles (which are service independent) are stored in a service
#     (that we will call AUTH) while permissions (which are service dependent) are store in the service database.
#     This is all good, but it creates a problem: when a user needs to authenticate, we need to send a request
#     (i.e., username, password) in AUTH service. AUTH service will return to us, among other information,
#     the user id and the user roles within an "access_token" (which is just a JWT token).
#
#     A frontend of a generic service will then need to send such "access_token" to its local database, managed by its
#     generic service backend. The backend will look at the JWT token, decode it and compute the permissions based
#     on the user and roles inside it.
#
#     Since permissions and roles may change, we need to persist them in our database.
#
#     Since django (see https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#handling-authorization-in-custom-backends)
#     use authentication backends in order to retrieve permissions, we create a backend which we can use to
#     retrieve user permissions: these are implemented in get_user_permissions, get_group_permissions
#
#     This backend is designed to be mounted only on the backend of the generic service.
#     Note that the actual user authentication (username and password) is not invoked here: that is the job of
#     user-auth-service. This backend consider an "access_token" that is assumed to specify the username and the roles
#     ( i.e., the token generated by user-auth-service).
#     If so, it synchronizes the database of the generic service and yield an api_token. The api_token generated
#     specifies permissions (both for role and for specific user).
#
#     If we don't receive the access_token, this backend fails. If you want an access token, you need to call
#     the auth-user-service first.
#     Since the only thing this backends needs is a JWT token, it makes sense to reuse the stuff present in
#     graphene-jwt. The authentication mechanism is the same one. However, we customize JWT_PAYLOAD_GET_USERNAME_HANDLER
#     and JWT_GET_USER_BY_NATURAL_KEY_HANDLER: the first is used by graphene-jwt to fetch the username from the handler
#     and the second one is used to fetch the user from the username. Here,
#     we use such functions to synchronize the database permissions. Note that the decoding mechanism needs to be
#     the same as the encoding mechanism of the user-auth-service.
#     The username in graphene-jwt can be whatver you want. So we return the whole payload (if user is found,
#     otherwise None to preserve graphene-jwt logic flow). The whole payload is then fed into JWT_GET_USER_BY_NATURAL_KEY_HANDLER
#     which will perform the synchronization.
#
#     At that point we need to yield an User instance as well as user permissions (since the authentication is succeeded).
#     JWT_GET_USER_BY_NATURAL_KEY_HANDLER fetches the information of group permissions and user permissions from the general
#     service local database. Since User table is not present and we need to retrieve a User instance and
#     since such data is not needed here, but is needed when requesting permissions of a user
#     (from all authentication backends, included this one), we use a django cache to index the permissions based
#     on the user: in this way we avoid manually adding a user table in the general service, which save space.
#     This cache is then used after authentication to fetch permission information by calling all authentication backends.
#     This is why we also implement the get_permissions_xxx methods: we manually override them to look inside the
#     user cache in order to fetch permission information.
#
#     The cache should be indexed both using user_id (which we have it) and api_token (which is generated at the end
#     of the json web authentication cycle). Here we focus on create the user in the cache, assigning it the permissions
#     from the roles.
#
#     The backend assume you tweak JsonWebToken in several ways:
#      - customization of jwt_decoder_handler
#      - customization of jwt_payload_get_username
#      - customization of user_by_natural_key_handler
#      - present of a cache where to save users called "users"
#      - decoration of access token mutation with annotation "token_auth_via_access_token",
#
#     The backend will add to the
#     """
#
#     @property
#     def cache_name(self) -> str:
#         return "users"
#
#     def authenticate(self, request, **kwargs) -> Optional[AuthUser]:
#         # Relay the request to the JSONWebTokenBackend super
#         # the backend will not authenticate if request._jwt_token_auth is set to True. The flag is set
#         # in token_auth authentication. If request._jwt_token_auth is True, it means that we want to authenticate
#         # using another authentication mechanism, not using the JSONWebTokenBackend one.
#         # We set it false and then reset it to whatever value
#         if hasattr(request, "_jwt_token_auth"):
#             old_value = request._jwt_token_auth
#             request._jwt_token_auth = False
#         result = JSONWebTokenBackend.authenticate(self, request, **kwargs)
#         if hasattr(request, "_jwt_token_auth"):
#             request._jwt_token_auth = old_value
#         return result
#
#     def get_user(self, user_id: TUSER_ID) -> Optional[AuthUser]:
#         return JSONWebTokenBackend.get_user(self, user_id)
#
#     def get_user_permissions(self, user_obj: AuthUser, obj=None) -> Set[TPERMISSION]:
#         # we have populate the cache during authentication. We just fetch permissions
#         cache: UserCache = caches[self.cache_name]
#         return cache.get_user_permissions(user_id=user_obj.id)
#
#     def get_group_permissions(self, user_obj: AuthUser, obj=None) -> Set[TPERMISSION]:
#         cache: UserCache = caches[self.cache_name]
#         return cache.get_group_permissions(user_id=user_obj.id)
#
#     # def get_user(self, user_id):
#     #     return None
#     #
#     # def get_user_permissions(self, user_obj: "AbstractGenericUser", obj=None):
#     #     self._synchronize_permission_to_user(user_obj)
#     #     return user_obj.user_permissions.all()
#     #
#     # def get_group_permissions(self, user_obj: "AbstractGenericUser", obj=None):
#     #     self._synchronize_permission_to_user(user_obj)
#     #     user_groups_field = get_user_model()._meta.get_field('groups')
#     #     user_groups_query = 'group__%s' % user_groups_field.related_query_name()
#     #     return Permission.objects.filter(**{user_groups_query: user_obj})
#     #
#     # def _synchronize_permission_to_user(self, user_obj: "AbstractGenericUser") -> "AbstractGenericUser":
#     #     """
#     #     Check if roles have already been added to the user.
#     #     If not, adds them
#     #     :param user_obj: user whose permissions we need to add
#     #     :return:
#     #     """
#     #
#     #     if (len(user_obj.groups) + len(user_obj.user_permissions)) > 0:
#     #         return user_obj
#     #     # try to fetch group information
#     #     self._update_user_roles_permissions(user_obj)
#     #
#     # def _update_user_roles_permissions(self, user_obj: "AbstractGenericUser") -> Dict[str, any]:
#     #     """
#     #     Ask the user auth service about the user roles
#     #     :param user_obj: the user whose permissions we need to fetch. Since weneed to contact an authenticated
#     #     backend, we need to pass an access token
#     #     :return:
#     #     """
#     #
#     #     client = GrapheneClient(schema=schema)
#     #     result = client.execute(f"""
#     #     query {{
#     #           me(token: "{user_obj.access_token}") {{
#     #             permissions {{
#     #                 id
#     #                 name
#     #             }}
#     #             groups {{
#     #                 id
#     #                 name
#     #                 permissions {{
#     #                     id
#     #                     name
#     #                 }}
#     #             }}
#     #           }}
#     #         }}
#     #     """)
#     #
#     #     return result
#
#
# # def _update_user_cache(f, fargs, fkwargs, dargs, dkwargs):
# #     # we need to add the token to the request, since we need inside our custom authentication backend (GeneralServiceAuthenticationBackend):
# #     # we have no way to fetch it inside the authenticate function
# #     fargs[2].context.access_token = fkwargs["token"]
# #     result = f(*fargs, **fkwargs)
# #     # in this result there should be the api_token. We need to fetch it and use it to update the user cache
# #     api_token = ""
# #
# #     cache: UserCache = caches[get_cache_name()]
# #     user: AuthUser = None
# #     cache.update_user_indexed_token(user, api_token)
# #
# #     return result
#
#
# # def update_user_cache(f):
# #     @functools.wraps(f)
# #     def decorator(*args, **kwargs):
# #         # graphql-jwt requires a password to be injected, however if it is null we will look at the token
# #         kwargs["password"] = None
# #         return _update_user_cache(f, args, kwargs, [], {})
# #     return decorator
#
#
# decorator copied by auth_token
def token_auth_via_access_token(payload_name: str, user_name: str, refresh_expires_in_name: str, token_output_name: str, cache_name: str):
    """

    :param payload_name:
    :param user_name:
    :param refresh_expires_in_name:
    :param token_output_name: name of the return value representing the token
    :param cache_name: name fo the cache where we will store user information
    :return:
    """
    def decorator(f):
        """
        Allows you to perform authentication via access token
        :param f:
        :return:
        """
        @functools.wraps(f)
        @setup_jwt_cookie
        @csrf_rotation
        @refresh_expiration_ex(refresh_expires_in_name)
        def wrapper(cls, root, info, token, **kwargs):
            context = info.context
            context._jwt_token_auth = True
            username = kwargs.get(get_user_model().USERNAME_FIELD)

            user = authenticate(
                request=context,
                token=token,
                **kwargs
            )
            if user is None:
                raise exceptions.JSONWebTokenError(
                    _('Please enter valid credentials'),
                )

            if hasattr(context, 'user'):
                context.user = user

            result = f(cls, root, info, **kwargs)
            signals.token_issued.send(sender=cls, request=context, user=user)
            result = maybe_thenable((context, user, result), on_token_auth_resolve)
            # the generated token is inside result.token
            api_token = result.token

            # update the cache by associating the api token to the user generated (but only if the user is not none!)
            cache: UserCache = caches[cache_name]
            user: AuthUser = cache.get_user_by_id(user.id)
            cache.update_user_indexed_token(user, api_token)

            # however, we need to set in the result the same field values that are declared in the graphql type of the login,
            # namely registry_payload and registry_user
            setattr(result, payload_name, result.payload)
            setattr(result, token_output_name, api_token)
            setattr(result, user_name, user)

            # set the just already authenticated user in request.authenticated_user as backup.
            # why? because the JSonTokenMiddleware messes with the standard context.user and overrides the already authenticated
            # user with the anonymous user.

            context.authenticated_user = user

            return result
        return wrapper
    return decorator


def refresh_expiration_ex(refresh_expires_in_name: str):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(cls, *args, **kwargs):
            def on_resolve(payload):
                val = (
                    timegm(datetime.utcnow().utctimetuple()) +
                    jwt_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()
                )
                setattr(payload, refresh_expires_in_name, val)
                return payload

            result = f(cls, *args, **kwargs)
            return maybe_thenable(result, on_resolve)
        return wrapper
    return decorator
#
# # update_user_cache = decorators.create_stateless_decorator(_update_user_cache)
# # update_user_cache.__doc__ = """
# #     Request to syhnchronize the cache with the user and group permissions.
# #     You should use this method to decoare token_auth authentication wrapper.
# #
# #     This function just link the api_token geneated by graphql-jwt with the cached user
# #     (generated during authentication phase)
# #     :param f:
# #     :return:
# #     """
#
#
# class GeneralServiceBackendJWTDecoderOutput(object):
#     """
#     Class used to transmit information between JWT custom functions
#     """
#
#     def __init__(self, payload, token: str):
#         self.payload = payload
#         self.token = token
#
#
# def jwt_payload_handler(user, context=None):
#     """
#
#     :param user: authenticated user
#     :param context:
#     :return:
#     """
#     result = graphql_jwt_utils.jwt_payload(user, context)
#
#     result["sub"] = user.id
#     return result
#
#
# def jwt_decoder_handler(token, context) -> GeneralServiceBackendJWTDecoderOutput:
#     """
#     Methdo used in place of JWT_DECODE_HANDLER
#     :param token: jwt token in input to decode
#     :param context: context fo the operaiton. Ususally request
#     :return: something that will be fed into JWT_PAYLOAD_GET_USERNAME_HANDLER
#     """
#     payload = graphjwt_utils.jwt_decode(token, context)
#     return GeneralServiceBackendJWTDecoderOutput(payload, token)
#
#
# def jwt_payload_get_username(decoding_output: GeneralServiceBackendJWTDecoderOutput) -> GeneralServiceBackendJWTDecoderOutput:
#     """
#     Method used in place of JWT_PAYLOAD_GET_USERNAME_HANDLER.
#     We use it to check if all the fields requird are defined
#
#     :param decoding_output: output of JWT_PAYLOAD_GET_USERNAME_HANDLER
#     :return: something that wil be fed into JWT_GET_USER_BY_NATURAL_KEY_HANDLER. Here it is the input itself
#     """
#
#     actual_token_payload = decoding_output.payload
#     for x in ("username", "sub", "roles"):
#         if x not in actual_token_payload:
#             LOG.warning(f"Ignoring token, since the claim {x} is not present")
#             return None
#     return decoding_output
#
#
# def user_by_natural_key_handler(decoding_output: GeneralServiceBackendJWTDecoderOutput) -> any:
#     """
#     Method used inplace of JWT_GET_USER_BY_NATURAL_KEY_HANDLER.
#     This method will **change** the database and adds the user if not existent. This occurs because the local
#     database of the service is just a "cache" of the generic service and is used only to
#     :param decoding_output: it is actually the whole payload of the jwt token we have received from the foreign
#     authentication service
#     :return: a structure representing the user
#     """
#
#     # fetch the model representing the user
#
#     actual_token_payload = decoding_output.payload
#     token = decoding_output.token
#     username = actual_token_payload["username"]
#     user_id = actual_token_payload["sub"]
#     roles = actual_token_payload["roles"]
#
#     # fetch user permissions
#     user_permissions = _get_user_permissions(user_id)
#     group_permissions = set()
#     for r in roles:
#         group_permissions = group_permissions.union(_get_role_permissions(role_id=r["id"], role_name=r["name"]))
#     user = save_user_info_in_cache(
#         user_id=user_id,
#         username=username,
#         roles=roles,
#         user_permissions=user_permissions,
#         group_permissions=group_permissions
#     )
#
#     return user
#
#
# def _get_user_permissions(user_id: int) -> List[Permission]:
#     """
#     Fetches the permissions attached to the user
#     :param user_id: id of the user whose permissions we need to fetch
#     :return: list of permissions. Each permission has an id and a name
#     """
#     app_name = "django_cbim_general_service"
#     result = Permission.objects.raw(f"""
#         SELECT P.id
#         FROM `{app_name}.AuthUserPermission` AS UP INNER JOIN auth_permission AS P ON P.id=UP.permission_id
#         WHERE UP.user_id={int(user_id)}
#     """)
#     return list(result)
#
#
# def _get_role_permissions(role_id: int, role_name: str) -> List[Permission]:
#     app_name = "django_cbim_general_service"
#     result = Permission.objects.raw(f"""
#         SELECT P.id
#         FROM `{app_name}.GroupPermission` AS GP INNER JOIN auth_permission AS P ON P.id=GP.permission_id
#         WHERE GP.group_id={int(role_id)}
#     """)
#     return list(result)
#
#
# def get_cache_name() -> str:
#     """
#     Returns the cache name that we are going to use to store permissions
#     :return: name fo the cache to use
#     """
#
#     return "users"
#
#
# def save_user_info_in_cache(user_id: int, username: str, roles: List[Dict[str, any]], user_permissions: List[Permission], group_permissions: Set[Permission]) -> AuthUser:
#     """
#     Overrideable. Save the user to the database or in another place.
#     We first fetch the information of user_permissions and roles_permissions. Then we add them all in
#     the user cache.
#
#     :param user_id: id of the user to save. Comes from the authentication service
#     :param username: username of the user to save. Comes from the authentication service
#     :param roles: roles of the user to save. dictionaries of id (int) and name (str)
#     :param user_permissions: lits of permissions associated to the user
#     :param group_permissions: list of permissions associated to every group containing the user
#     :param token: access token
#     :return: user object. Information about the user has been successfully updated
#     """
#     cache: UserCache = caches[get_cache_name()]
#     user = AuthUser(
#         id=user_id,
#         username=username
#     )
#     # fetch all the user_roles and user_permissions
#     cache.update_user_indexed_primary_key(user, roles, user_permissions, group_permissions)
#     return user
#
#
#
#
#
