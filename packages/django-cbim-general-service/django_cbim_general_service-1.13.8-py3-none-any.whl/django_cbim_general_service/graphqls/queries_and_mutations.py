import abc
from builtins import classmethod
from datetime import timedelta
from typing import Tuple, Union, List, Dict, Optional

import graphene
import graphql_jwt
import stringcase
from django_graphene_authentication.queries_and_mutations import AbstractAccessTokenGeneratorMutationCreator
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.graphql_decorators import graphql_submutation
from graphene.types.generic import GenericScalar
from graphql_jwt import mixins, JSONWebTokenMutation
from graphql_jwt.decorators import token_auth
from graphql_jwt.middleware import JSONWebTokenMiddleware
from graphql_jwt.mixins import JSONWebTokenMixin
from graphql_jwt.settings import jwt_settings
from django_cbim_general_service.conf import settings

from django_cbim_general_service.backends import token_auth_via_access_token

import logging

LOG = logging.getLogger(__name__)


class AbstractGeneralServiceAccessTokenGeneratorMutationCreator(AbstractAccessTokenGeneratorMutationCreator, abc.ABC):
    """
    A class that allows you to create query and mutations for login purposes.

    This class should be used ot create queries and mutation for a general CBIM service (not user-auth-service!).
    Usually  CBIM services requires to contact a user-auth-service to fetch an access_token.
    Then we use the access_token to contact hte local database to create an api_token, which is then use to validate
    all next service requests.
    """

    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name

    @abc.abstractmethod
    def user_graphene_type(self):
        """
        Each service can override the type representing the user (e.g., by agumenting its permissions)
        This method will return the graphene type represenitng the user (e.g., AuthUserGraphQLType)
        :return:
        """
        pass

    def me_query_return_type(self, context):
        """
        The return type of hte /me query. Usually it should return the user currently authenticated
        (e.g., AuthUserGraphQLType)

        :param context: shared context used when creating the queries and mutation of the service
        :return:
        """
        return self.user_graphene_type()

    def me_query_class_name(self, context) -> str:
        return stringcase.camelcase(f"{self.service_name}UserMeQuery")

    def me_query_return_value_name(self, context) -> any:
        return stringcase.camelcase(f"{self.service_name}UserMe")

    def get_permissions_required_to_me_query(self, context) -> Union[str, List[str]]:
        return []

    def _login_mutation_user_resolver_name(self) -> str:
        return stringcase.camelcase(f"{self.service_name}User")

    def _login_mutation_return_type(self, context) -> Dict[str, any]:
        # adds user field
        result = super()._login_mutation_return_type(context)
        result[self._login_mutation_user_resolver_name()] = GraphQLHelper.returns_nonnull(self.user_graphene_type(), f"user of service {self.service_name} just authenticated")
        return result

    def login_generate_mutation_output(self, user, mutation_instance, info, *args, **kwargs):
        return mutation_instance(**{self._login_mutation_user_resolver_name(): user})

    def login_mutation_class_name(self, context) -> str:
        return f"{self.service_name}Login"

    def jwt_generated_payload_name(self) -> str:
        return stringcase.snakecase(f"{self.service_name}LoginPayload")

    def jwt_generated_refresh_expires_in_name(self) -> str:
        return stringcase.snakecase(f"{self.service_name}RefreshExpiresIn")

    def jwt_generated_token_name(self) -> str:
        return stringcase.snakecase(f"{self.service_name}ApiToken")

    def jwt_generated_long_running_refresh_token_name(self) -> str:
        return stringcase.snakecase(f"{self.service_name}LongRunningRefreshToken")

    def jwt_generated_long_running_refresh_token(self) -> bool:
        return False

    def jwt_generated_allow_refresh(self) -> bool:
        return True

    def jwt_generated_audience(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_AUDIENCE"]

    def jwt_generated_issuer(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_ISSUER"]

    def jwt_generated_token_algorithm(self) -> str:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_ALGORITHM"]

    def jwt_generated_token_secret_key(self) -> str:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_SECRET_KEY"]

    def jwt_generated_token_public_key(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_PUBLIC_KEY"]

    def jwt_generated_token_private_key(self) -> Optional[str]:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_PRIVATE_KEY"]

    def jwt_generated_reuse_refresh_tokens(self) -> bool:
        return False

    def jwt_generated_token_expiration_time(self) -> timedelta:
        return settings.DJANGO_CBIM_GENERAL_SERVICE["JWT_API_TOKEN_EXPIRATION_TIME"]

    def jwt_use_csrf_rotation(self) -> bool:
        return False


def generate_json_web_token_mixin_class(prefix: str, payload_name: str, refresh_expires_in_name: str, token_output_name: str):

    result: type

    def field(cls, *args, **kwargs):
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields[token_output_name] = graphene.Field(graphene.String, required=True)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields[refresh_expires_in_name] =\
                    graphene.Field(graphene.String, required=True)

        return super(result, cls).Field(*args, **kwargs)

    result = type(
        f"{prefix}JSONWebTokenMixin",
        (),
        {
            payload_name: GenericScalar(required=True),
            refresh_expires_in_name: graphene.Int(required=True),
            "Field": classmethod(field)
        }
    )
    return result


def generate_obtain_json_web_token_mixin(prefix: str, payload_name: str, refresh_expires_in_name: str, token_output_name: str):
    result: type = None

    def __init_subclass_with_meta__(cls, name=None, **options):
        assert getattr(cls, 'resolve', None), (
            f'{name or cls.__name__}.resolve '
            f'method is required in a {prefix}JSONWebTokenMutation.'
        )
        # with just super() the chain did not work. I'm not very confident in super(result, cls) class
        super(result, cls).__init_subclass_with_meta__(name=name, **options)

    result = type(
        f"{prefix}ObtainJSONWebTokenMixin",
        (generate_json_web_token_mixin_class(prefix=prefix, payload_name=payload_name, refresh_expires_in_name=refresh_expires_in_name, token_output_name=token_output_name),),
        {
            "__init_subclass_with_meta__": classmethod(__init_subclass_with_meta__)
        }
    )
    return result


def generate_login_with_access_token_mutation(base_name: str, graphene_user_type: type, class_name: str = None, user_name: str = None, payload_name: str = None, refresh_expires_in_name: str = None, api_token_name: str = None, access_token_name: str = None, add_token_param: bool = True):
    """
    Create a mutation class that allow the user to authenticate via a single access token.
    The token can either be sent using a (optional) graphql argument or via Authorization header

    :param base_name: string used as prefix in automatic class name generation
    :param graphene_user_type: type of the user derivign from graophene.ObjectType
    :param class_name: if present, the name of the mutation class to generate
    :param user_name: if present, the name of the mutation output repersenting the user
    :param payload_name: if present, the name of the mutation output representing the JWT payload
    :param refresh_expires_in_name: if present, the name of the mutation output representing the refresh expires name
    :param api_token_name: name of the return value representing the api token
    :param access_token_name: name of the token in the mutation argument
    :param add_token_param: if true, we will add an optional token parameter at the end of the graphql mutation
    :return: the mutation class representing the login via access token
    """
    if class_name is None:
        class_name = stringcase.pascalcase(f"{base_name}LoginWithAccessToken")
    if user_name is None:
        user_name = stringcase.snakecase(f"{base_name}User")
    if payload_name is None:
        payload_name = stringcase.snakecase(f"{base_name}Payload")
    if refresh_expires_in_name is None:
        refresh_expires_in_name = stringcase.snakecase(f"{base_name}RefreshExpiresIn")
    if api_token_name is None:
        api_token_name = stringcase.snakecase(f"{base_name}ApiToken")
    if access_token_name is None:
        access_token_name = jwt_settings.JWT_ARGUMENT_NAME
    else:
        access_token_name = "access_token"

    def resolve(cls, root, info, **kwargs):
        return cls(**{user_name: info.context.user})

    result: type

    def field(cls, *args, **kwargs):
        # arguments of the authentication mutation. Generated by diffing graphql_jwt.mutations.JSONWebTokenMutation
        # and manually remove username and password required fields. We only need to inject the "token", which
        # is automatically added
        cls._meta.arguments.update({
            access_token_name: graphene.String(required=False, description=f"""Token generated by the user authentication server. 
                If left unspecified, we will fetch the token from the 
                Authorization header with domain {jwt_settings.JWT_AUTH_HEADER_PREFIX}""")
        })
        return super(result, cls).Field(*args, **kwargs)

    @token_auth_via_access_token(payload_name=payload_name, user_name=user_name,
                                 refresh_expires_in_name=refresh_expires_in_name, token_output_name=api_token_name, cache_name="users")
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)

    result = type(
        class_name,
        (generate_obtain_json_web_token_mixin(class_name, payload_name, refresh_expires_in_name, token_output_name=api_token_name), graphene.Mutation, ),
        {
            user_name: graphene.Field(graphene_user_type, description=f"user that has just requested authentication for service {base_name}"),
            "resolve": classmethod(resolve),
            "Field": classmethod(field),
            "mutate": classmethod(mutate),
        }
    )
    return result


def create_login_graphql_endpoints(service_name: str, user_type: type, access_token_name: str = None, api_token_name: str = None) -> Tuple[type, type, type, type]:
    """
    Generate the authentication graphql queries and mutations needed  for a general service
    :param service_name: name of the service
    :param user_type: graphql type repersenting a user
    :param access_token_name: name of the token used to authenticate the login. If left missing, it is "token"
    :param api_token_name: name of the token generated by the login mutation.
    :return: tuple with the following graphql queries and mutations:
     - login mutation (accept token);
     - verify mutation;
     - refresh mutation;
     - query me;
    """

    login = graphql_submutation(generate_login_with_access_token_mutation(
        base_name=stringcase.pascalcase(service_name),
        graphene_user_type=user_type,
        add_token_param=True,
        api_token_name=api_token_name,
        access_token_name=access_token_name,
    ))

    # verify = type(
    #     f"{stringcase.pascalcase(service_name)}VerifyToken",
    #     (object, ),
    #     {
    #         "__doc__": f"""
    #         verify that a token yielded by {stringcase.sentencecase(service_name)} is indeed valie
    #         """,
    #         f"{stringcase.snakecase(service_name)}_verify_token": graphql_jwt.Verify.Field(description=f"Verify an already generated api token yielded by {stringcase.sentencecase(service_name)}"),
    #     }
    # )
    # verify = graphql_submutation(verify)
    #
    # refresh = type(
    #     f"{stringcase.pascalcase(service_name)}RefreshToken",
    #     (object,),
    #     {
    #         "__doc__": f"""
    #             refresh an already yielded token generated by {stringcase.sentencecase(service_name)}
    #             """,
    #         f"{stringcase.snakecase(service_name)}_refresh_token": graphql_jwt.Refresh.Field(
    #             description=f"Verify an already generated api token yielded by {stringcase.sentencecase(service_name)}"),
    #     }
    # )
    # refresh = graphql_submutation(refresh)

    def resolve_me(cls, info, **kwargs):
        result = info.context.user
        return result

    me = GraphQLHelper.create_authenticated_query(
        query_class_name=f"{stringcase.pascalcase(service_name)}Me",
        description="""
        Query allowing you to retrieve the information regarding the currently authenticated user
        """,
        arguments={},
        return_type=user_type,
        body=resolve_me,
        permissions_required=[],
        add_token=True,
        token_name=api_token_name
    )

    return login, None, None, me




# from builtins import classmethod
# from typing import Tuple
#
# import graphene
# import graphql_jwt
# import stringcase
# from django_koldar_utils.graphql.GraphQLHelper import GraphQLHelper
# from django_koldar_utils.graphql.graphql_decorators import graphql_submutation
# from graphene.types.generic import GenericScalar
# from graphql_jwt import mixins, JSONWebTokenMutation
# from graphql_jwt.decorators import token_auth
# from graphql_jwt.middleware import JSONWebTokenMiddleware
# from graphql_jwt.mixins import JSONWebTokenMixin
# from graphql_jwt.settings import jwt_settings
#
# from django_cbim_general_service.backends import token_auth_via_access_token
#
# import logging
#
# LOG = logging.getLogger(__name__)
#
#
# def generate_json_web_token_mixin_class(prefix: str, payload_name: str, refresh_expires_in_name: str, token_output_name: str):
#
#     result: type
#
#     def field(cls, *args, **kwargs):
#         if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
#             cls._meta.fields[token_output_name] = graphene.Field(graphene.String, required=True)
#
#             if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
#                 cls._meta.fields[refresh_expires_in_name] =\
#                     graphene.Field(graphene.String, required=True)
#
#         return super(result, cls).Field(*args, **kwargs)
#
#     result = type(
#         f"{prefix}JSONWebTokenMixin",
#         (),
#         {
#             payload_name: GenericScalar(required=True),
#             refresh_expires_in_name: graphene.Int(required=True),
#             "Field": classmethod(field)
#         }
#     )
#     return result
#
#
# def generate_obtain_json_web_token_mixin(prefix: str, payload_name: str, refresh_expires_in_name: str, token_output_name: str):
#     result: type = None
#
#     def __init_subclass_with_meta__(cls, name=None, **options):
#         assert getattr(cls, 'resolve', None), (
#             f'{name or cls.__name__}.resolve '
#             f'method is required in a {prefix}JSONWebTokenMutation.'
#         )
#         # with just super() the chain did not work. I'm not very confident in super(result, cls) class
#         super(result, cls).__init_subclass_with_meta__(name=name, **options)
#
#     result = type(
#         f"{prefix}ObtainJSONWebTokenMixin",
#         (generate_json_web_token_mixin_class(prefix=prefix, payload_name=payload_name, refresh_expires_in_name=refresh_expires_in_name, token_output_name=token_output_name),),
#         {
#             "__init_subclass_with_meta__": classmethod(__init_subclass_with_meta__)
#         }
#     )
#     return result
#
#
# def generate_login_with_access_token_mutation(base_name: str, graphene_user_type: type, class_name: str = None, user_name: str = None, payload_name: str = None, refresh_expires_in_name: str = None, api_token_name: str = None, access_token_name: str = None, add_token_param: bool = True):
#     """
#     Create a mutation class that allow the user to authenticate via a single access token.
#     The token can either be sent using a (optional) graphql argument or via Authorization header
#
#     :param base_name: string used as prefix in automatic class name generation
#     :param graphene_user_type: type of the user derivign from graophene.ObjectType
#     :param class_name: if present, the name of the mutation class to generate
#     :param user_name: if present, the name of the mutation output repersenting the user
#     :param payload_name: if present, the name of the mutation output representing the JWT payload
#     :param refresh_expires_in_name: if present, the name of the mutation output representing the refresh expires name
#     :param api_token_name: name of the return value representing the api token
#     :param access_token_name: name of the token in the mutation argument
#     :param add_token_param: if true, we will add an optional token parameter at the end of the graphql mutation
#     :return: the mutation class representing the login via access token
#     """
#     if class_name is None:
#         class_name = stringcase.pascalcase(f"{base_name}LoginWithAccessToken")
#     if user_name is None:
#         user_name = stringcase.snakecase(f"{base_name}User")
#     if payload_name is None:
#         payload_name = stringcase.snakecase(f"{base_name}Payload")
#     if refresh_expires_in_name is None:
#         refresh_expires_in_name = stringcase.snakecase(f"{base_name}RefreshExpiresIn")
#     if api_token_name is None:
#         api_token_name = stringcase.snakecase(f"{base_name}ApiToken")
#     if access_token_name is None:
#         access_token_name = jwt_settings.JWT_ARGUMENT_NAME
#     else:
#         access_token_name = "access_token"
#
#     def resolve(cls, root, info, **kwargs):
#         return cls(**{user_name: info.context.user})
#
#     result: type
#
#     def field(cls, *args, **kwargs):
#         # arguments of the authentication mutation. Generated by diffing graphql_jwt.mutations.JSONWebTokenMutation
#         # and manually remove username and password required fields. We only need to inject the "token", which
#         # is automatically added
#         cls._meta.arguments.update({
#             access_token_name: graphene.String(required=False, description=f"""Token generated by the user authentication server.
#                 If left unspecified, we will fetch the token from the
#                 Authorization header with domain {jwt_settings.JWT_AUTH_HEADER_PREFIX}""")
#         })
#         return super(result, cls).Field(*args, **kwargs)
#
#     @token_auth_via_access_token(payload_name=payload_name, user_name=user_name,
#                                  refresh_expires_in_name=refresh_expires_in_name, token_output_name=api_token_name, cache_name="users")
#     def mutate(cls, root, info, **kwargs):
#         return cls.resolve(root, info, **kwargs)
#
#     result = type(
#         class_name,
#         (generate_obtain_json_web_token_mixin(class_name, payload_name, refresh_expires_in_name, token_output_name=api_token_name), graphene.Mutation, ),
#         {
#             user_name: graphene.Field(graphene_user_type, description=f"user that has just requested authentication for service {base_name}"),
#             "resolve": classmethod(resolve),
#             "Field": classmethod(field),
#             "mutate": classmethod(mutate),
#         }
#     )
#     return result
#
#
# def create_login_graphql_endpoints(service_name: str, user_type: type, access_token_name: str = None, api_token_name: str = None) -> Tuple[type, type, type, type]:
#     """
#     Generate the authentication graphql queries and mutations needed  for a general service
#     :param service_name: name of the service
#     :param user_type: graphql type repersenting a user
#     :param access_token_name: name of the token used to authenticate the login. If left missing, it is "token"
#     :param api_token_name: name of the token generated by the login mutation.
#     :return: tuple with the following graphql queries and mutations:
#      - login mutation (accept token);
#      - verify mutation;
#      - refresh mutation;
#      - query me;
#     """
#
#     login = graphql_submutation(generate_login_with_access_token_mutation(
#         base_name=stringcase.pascalcase(service_name),
#         graphene_user_type=user_type,
#         add_token_param=True,
#         api_token_name=api_token_name,
#         access_token_name=access_token_name,
#     ))
#
#     # verify = type(
#     #     f"{stringcase.pascalcase(service_name)}VerifyToken",
#     #     (object, ),
#     #     {
#     #         "__doc__": f"""
#     #         verify that a token yielded by {stringcase.sentencecase(service_name)} is indeed valie
#     #         """,
#     #         f"{stringcase.snakecase(service_name)}_verify_token": graphql_jwt.Verify.Field(description=f"Verify an already generated api token yielded by {stringcase.sentencecase(service_name)}"),
#     #     }
#     # )
#     # verify = graphql_submutation(verify)
#     #
#     # refresh = type(
#     #     f"{stringcase.pascalcase(service_name)}RefreshToken",
#     #     (object,),
#     #     {
#     #         "__doc__": f"""
#     #             refresh an already yielded token generated by {stringcase.sentencecase(service_name)}
#     #             """,
#     #         f"{stringcase.snakecase(service_name)}_refresh_token": graphql_jwt.Refresh.Field(
#     #             description=f"Verify an already generated api token yielded by {stringcase.sentencecase(service_name)}"),
#     #     }
#     # )
#     # refresh = graphql_submutation(refresh)
#
#     def resolve_me(cls, info, **kwargs):
#         result = info.context.user
#         return result
#
#     me = GraphQLHelper.create_authenticated_query(
#         query_class_name=f"{stringcase.pascalcase(service_name)}Me",
#         description="""
#         Query allowing you to retrieve the information regarding the currently authenticated user
#         """,
#         arguments={},
#         return_type=user_type,
#         body=resolve_me,
#         permissions_required=[],
#         add_token=True,
#         token_name=api_token_name
#     )
#
#     return login, None, None, me
#
#
