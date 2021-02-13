from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = 'catalog'
    verbose_name = 'Каталог'

    def ready(self):
        # pylint: disable=unused-import,import-outside-toplevel
        from . import signals