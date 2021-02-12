from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.contrib.staticfiles import apps as static_apps


class CoreConfig(AppConfig):
    name = 'core'


# Configurations for apps located outside of the project's root directory
# (e.g. django.contrib apps and packages installed using Pip).


class MainAdminConfig(AdminConfig):
    default_site = 'core.admin.get_main_adminsite'


class StaticFilesConfig(static_apps.StaticFilesConfig):
    ignore_patterns = [
        '*/src/*',
        '*.js.map',
        '*.css.map',
    ]