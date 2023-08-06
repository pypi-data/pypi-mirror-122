import os
from datetime import timedelta

from django.conf import settings
from appconf import AppConf


class DjangoCbimGeneralServiceAppConf(AppConf):
    class Meta:
        prefix = "DJANGO_CBIM_GENERAL_SERVICE"
        #holder = "django_app_graphql.conf.settings"

    JWT_API_TOKEN_AUDIENCE: str = None
    JWT_API_TOKEN_ISSUER: str = None
    JWT_API_TOKEN_ALGORITHM: str = "HS256"
    JWT_API_TOKEN_SECRET_KEY: str = None
    JWT_API_TOKEN_PUBLIC_KEY: str = None
    JWT_API_TOKEN_PRIVATE_KEY: str = None
    JWT_API_TOKEN_EXPIRATION_TIME: timedelta = timedelta(hours=60)

