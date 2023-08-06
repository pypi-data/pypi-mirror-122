import abc
from datetime import timedelta
from typing import List, Dict, Optional, Iterable, Tuple
from django.conf import settings
from urllib import parse

import os

from django_koldar_utils.django_toolbox.settings import settings_helper
from django_koldar_utils.django_toolbox.settings.AbstractSettingsGenerator import AbstractGraphQLSettingsGenerator
from django_koldar_utils.models.AttrDict import AttrDict


class CBIMSettingsGenerator(AbstractGraphQLSettingsGenerator):
    """
    A settings generator that creates a settings.py file uimmediately usable to deploy a CBIM general service
    """

    def __init__(self, interesting_services: List[str], authentication_mechanisms: List[str], aws_url: str, middlewares_to_append: List[str] = None):
        """

        :param interesting_services:
        :param authentication_mechanisms:
        :param aws_url: url yielded by zappa deploy
        :param middlewares_to_append:
        """

        super().__init__()
        self.interesting_services = interesting_services
        self.middlewares_to_append = middlewares_to_append or []
        self.authentication_mechanisms = authentication_mechanisms
        self.aws_url = aws_url

    @property
    def app_service(self) -> str:
        """

        :return: Name of the app that generates the service that we want to expose
        """
        return self.interesting_services[-1]

    def _configure_installed_apps(self, original: List[str]) -> List[str]:
        return add_cbim_service_installed_apps(original, self.interesting_services)

    def _configure_middlewares(self, original: List[str]) -> List[str]:
        original.extend(self.middlewares_to_append)
        return original

    def _generate_default_graphene_resolver_middlewares(self) -> List[str]:
        return [
            f"django_cbim_general_service.middleware.GeneralServiceApiTokenGraphQLAuthenticationMiddleware"
        ]

    def _configure_caches(self, original: Dict[str, any]) -> Dict[str, any]:
        original["users"] = {
                'BACKEND': 'django_cbim_general_service.cache.UserCache',
                'LOCATION': 'users',
                'TIMEOUT': '1h',
            }
        return original

    def _configure_authentication_backends(self) -> List[str]:
        return self.authentication_mechanisms

    def _get_auth_user_model(self) -> Optional[str]:
        return "django_cbim_general_service.AuthUser"

    def _get_apps_to_configure(self) -> Iterable[Tuple[str, str]]:
        yield from super()._get_apps_to_configure()
        yield ("DJANGO_CBIM_GENERAL_SERVICE", "django_cbim_general_service")

    def _configure_allowed_hosts(self, original: List[str]) -> List[str]:
        return settings_helper.allows_deploy_to_aws(
            url=self.aws_url,
            allowed_hosts=original
        )

    def _configure_app(self, settings_name: str, app_name: str, original_data: any) -> Optional[any]:
        result = super()._configure_app(settings_name, app_name, original_data)
        if result is not None:
            return result
        # standard
        if app_name == "django_cbim_general_service":
            return {
                "JWT_API_TOKEN_AUDIENCE": None,
                "JWT_API_TOKEN_ISSUER": None,
                "JWT_API_TOKEN_ALGORITHM": "HS256",
                "JWT_API_TOKEN_SECRET_KEY": self.env("API_TOKEN_SECRET_KEY"),
                "JWT_API_TOKEN_PUBLIC_KEY": None,
                "JWT_API_TOKEN_PRIVATE_KEY": None,
                "JWT_API_TOKEN_EXPIRATION_TIME": timedelta(hours=1),
                # needs to be the same of user-auth-service
                "ACCESS_TOKEN_SECRET_KEY": self.env("ACCESS_TOKEN_SECRET_KEY"),
                "ACCESS_TOKEN_PUBLIC_KEY": None,
                "ACCESS_TOKEN_AUDIENCE": None,
                "ACCESS_TOKEN_ISSUER": None,
                "ACCESS_TOKEN_ALGORITHM": self.env("ACCESS_TOKEN_ALGORITHM"),
            }


def add_cbim_service_installed_apps(installed_apps: List[str], interesting_services: List[str]) -> List[str]:
    """
    Modify the INSTALLED_APPS of settings to contain all the apps used to implement a generic cbim service.

    This will add the following:

     - cors;
     - graphql server endpoint
     - django_graphene_authentication
     - cbim commons and general service

    :param installed_apps: installed apps to update
    :param interesting_services: apps repersenting the services that you want to install typical of your cbim service
    :return: the new INSTALLED_APPS to have
    """

    result = list(installed_apps)
    # add cors as well
    # you need to add if you want Authorization header to be included in the request of the wsgi server
    result.insert(0, 'corsheaders')

    result.extend([
        # cbim apps all need this
        'django_cbim_commons',
        # cbim services using authentication need this
        'django_cbim_general_service',
        # graphql
        'graphene_django',
        'django_filters',
        'django_graphene_authentication',
    ])
    # apps that you should add to implement the service
    result.extend(interesting_services)
    result.extend([
        # make sure the django_app_graphql is the last app you add!
        'django_app_graphql',
    ])
    return result
