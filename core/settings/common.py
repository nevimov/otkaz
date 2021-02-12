"""Settings used as a base for other setting modules.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

# Build paths inside the project like this: str(BASE_DIR / 'foo-path')
BASE_DIR = PROJECT_PACKAGE.parent


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'core.apps.CoreConfig',
    'core.apps.MainAdminConfig', # django.contrib.admin custom config
    'core.apps.StaticFilesConfig',  # django.contrib.staticfiles custom config

    # Apps located inside the project's root directory
    'cities.apps.CitiesConfig',
    'accounts.apps.AccountsConfig',
    'catalog.apps.CatalogConfig',
    'contacts.apps.ContactsConfig',
    'sellers.apps.SellersConfig',

    # Pip packages
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ckeditor',
    'django_filters',
    'phonenumber_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'cities.context_processors.cities',
                'contacts.context_processors.contacts',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# ************
# *** Auth ***
# ************

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = 'sellers:profile'

LOGIN_URL = '/accounts/login/'

LOGOUT_REDIRECT_URL = 'account_login'


# ****************************
# *** Internationalization ***
# ****************************

LANGUAGE_CODE = 'ru'

LOCALE_PATHS = [
    str(BASE_DIR / 'locale'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ******************************
# *** Static and media files ***
# ******************************

STATIC_URL = '/static/'

MEDIA_URL = '/media/'


# ************************
# *** Third-party Apps ***
# ************************

# --- django-allatuh ---
#

ACCOUNT_AUTHENTICATION_METHOD = "username"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_PRESERVE_USERNAME_CASING = False

ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.SellerSignupForm'


# --- django-ckeditor ---
#

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'basic',
        'toolbar_basic': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['RemoveFormat']
        ],
        'width': 500,
        'height': 200,
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'autogrow',
            # 'autoembed',
            # 'autolink',
            # 'clipboard',
            # 'dialog',
            # 'dialogui',
            # 'div',
            # 'elementspath'
            # 'embedsemantic',
            # 'lineutils',
            # 'uploadimage'
            # 'widget',
        ]),


    },
    'advanced': {
        'toolbar': 'advanced',
        'toolbar_advanced': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}


# --- django-filter ---
#

FILTERS_EMPTY_CHOICE_LABEL = '--'


# --- phonenumbers-field ---
#

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'RU'


# ***********************
# *** Custom settings ***
# ***********************

# Protocol used to access sites powered by this django installation.
# The value is used to build full subdomain URLs (for example, URLs of
# city sites).
PROTOCOL = 'http'