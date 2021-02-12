"""Django settings for the development environment."""

from distutils.util import strtobool
from os import getenv

from .common import *  # pylint: disable=wildcard-import, unused-wildcard-import


DEBUG = True

ALLOWED_HOSTS = [
    '.localhost',
    '127.0.0.1',
    '[::1]',
    '0.0.0.0',  # For docker
]

SECRET_KEY = 'dummy-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB', 'postgres'),
        'HOST': getenv('POSTGRES_HOST', '127.0.0.1'),
        'PORT': getenv('POSTGRES_PORT', '5432'),
        'USER': getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': getenv('POSTGRES_PASSWORD', 'dummypass'),
    }
}

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'dummymailman@mail.ru'
EMAIL_HOST_PASSWORD = '-UyupB3rIKi2'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = '[отказные-окна.рф] '
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_ROOT = str(BASE_DIR / '.local/media-root')
STATIC_ROOT = str(BASE_DIR / '.local/static-root')


# ************************
# *** Third-party Apps ***
# ************************

# --- django-debug-toolbar ---
#

DEBUG_TOOLBAR = strtobool(getenv('DEBUG_TOOLBAR', 'no'))

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        'INSERT_BEFORE': '</main>',  # The default </body> brakes page layout
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,  # Fix for Docker
    }


# ***********************
# *** Custom settings ***
# ***********************

PROTOCOL = 'http'

DEV_MAIL = "nevimov@gmail.com"
FEEDBACK_REQUEST_RECIPIENTS = [DEV_MAIL]
CALLBACK_REQUEST_RECIPIENTS = [DEV_MAIL]