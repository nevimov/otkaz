"""Django settings for the production environment.

This module contains sensitive data, keep it secret!
"""
import json
import os

from .common import * # pylint: disable=wildcard-import, unused-wildcard-import

PROJECT_PARENT_DIR = BASE_DIR.parent
SECRETS_DIR = str(PROJECT_PARENT_DIR.joinpath('secrets'))


def get_secret(path, default=None):
    """
    Read a secret from a file with the given `path`.
    """
    secret_path = os.path.join(SECRETS_DIR, path)
    _, ext = os.path.splitext(secret_path)
    try:
        with open(secret_path) as handle:
            if ext == '.json':
                return json.load(handle)
            return handle.read().strip()
    except FileNotFoundError:
        if default is not None:
            return default
        raise RuntimeError(
            "Secret '%s' does not exist. "
            "The default value is not set either." % secret_path
        )


DEBUG = False

SECRET_KEY = get_secret('django/secret_key',
                        'dummy-secret-key-78342gg48s7f23g48f723g478g324gy273')

ALLOWED_HOSTS = [
    '.отказные-окна.рф',
] + get_secret('django/allowed_hosts.json', [])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('postgres/db'),
        'USER': get_secret('postgres/user'),
        'PASSWORD': get_secret('postgres/password'),
        'HOST': get_secret('postgres/host'),
        'PORT': get_secret('postgres/port'),
    }
}

EMAIL_HOST = get_secret('email/host')
EMAIL_HOST_USER = get_secret('email/user')
EMAIL_HOST_PASSWORD = get_secret('email/password')
EMAIL_PORT = get_secret('email/port', 465)
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = '[отказные-окна.рф] '
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_ROOT = str(PROJECT_PARENT_DIR.joinpath('media-root'))
STATIC_ROOT = str(PROJECT_PARENT_DIR.joinpath('static-root'))


# ***********************
# *** Custom settings ***
# ***********************

FEEDBACK_REQUEST_RECIPIENTS = ['nevimov@gmail.com']
CALLBACK_REQUEST_RECIPIENTS = ['nevimov@gmail.com']