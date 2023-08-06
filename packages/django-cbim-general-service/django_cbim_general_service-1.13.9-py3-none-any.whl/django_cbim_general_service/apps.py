from django.apps import AppConfig
from django_koldar_utils.functions import modules


class DjangoCbimGeneralServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_cbim_general_service'

    def ready(self):
        modules.import_module("django_cbim_general_service.graphqls.queries_and_mutations")
