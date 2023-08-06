from django_graphene_authentication.middleware import AbstractGraphQLAuthenticationMiddleware


class GeneralServiceApiTokenGraphQLAuthenticationMiddleware(AbstractGraphQLAuthenticationMiddleware):
    """
    Middleware used authenticate a graphql request not involving a login mutation
    """

    def jwt_allow_argument(self) -> bool:
        return True

    def jwt_api_token_name(self) -> str:
        return "api_token"

    def jwt_global_authenticate_in_graphql(self) -> bool:
        return True

    def jwt_global_graphql_user_field_name(self) -> str:
        return "authenticated_user"