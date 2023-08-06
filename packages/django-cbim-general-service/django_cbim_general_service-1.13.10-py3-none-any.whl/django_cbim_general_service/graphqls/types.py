# First decalre all the graphql you are going to use
# You may also decide to agument such schemas

# Agument a class that has been fetched from the graphene federation with other information.
# For instance, our user not only has associated groupes (which are provided by the same service
# holding users) but permissions as well. Each agumented information required a tuned resolvers
# Let assume you have a service A providing AuthUserGraphQLType and service B extending such a type with "permissions"
# (alongside other types). in service A, AuthUserGraphQLTypeneeds to be deocrated with @key. In service B,
# we need to decorate AuthUserGraphQLType with "extend", and set the id that we are going to use to connect as external.
# Adding a "resolve_id" method for the class is optional and can be used to inject code
# when an id has been resolved, the graphql gateway will query the service owning the particular object.
from django.contrib.auth.models import Permission
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from graphene import ObjectType
from graphene_django import DjangoObjectType
from graphene_federation import external, extend, key
from graphql_jwt.decorators import login_required


@key("id")
class AuthPermissionGraphQLType(DjangoObjectType):
    class Meta:
        model = Permission

    def __resolve_reference(self, info, **kwargs):
        if self.id is not None:
            return Permission.objects.get(id=int(self.id))
        else:
            raise ValueError(f"Invalid permission identifier {self}")