"""
Django settings for manager project.

Generated by 'django-admin startproject' using Django 2.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import dj_database_url
from distutils.util import strtobool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.environ.get('DEBUG', 'false')))

# If set to True, Django's normal exception handling of view functions
# will be suppressed, and exceptions will propagate upwards
# https://docs.djangoproject.com/en/2.2/ref/settings/#debug-propagate-exceptions
DEBUG_PROPAGATE_EXCEPTIONS = True

# Enable Django admin
ADMIN_ENABLED = bool(strtobool(os.environ.get('ADMIN_ENABLED', 'false')))

# Enable drycc legal footer
LEGAL_ENABLED = bool(strtobool(os.environ.get('LEGAL_ENABLED', 'false')))
# Drycc Billing details
BILLING_DETAILS = {
    "name": "DOOPAI LTD",
    "email": "support@drycc.com",
    "phone": "+447418360823",
    "address": {
        "line1": '20 Guild Rd',
        "line2": '',
        "city": 'London',
        "state": 'England',
        "country": 'UK',
        "postcode": 'SE7 8HN'
    },
}

# Silence two security messages around SSL as router takes care of them
# https://docs.djangoproject.com/en/2.2/ref/checks/#security
SILENCED_SYSTEM_CHECKS = [
    'security.W004',
    'security.W008',
    'security.W012',
    'security.W016',
]

CONN_MAX_AGE = 60 * 3

# SECURITY: change this to allowed fqdn's to prevent host poisioning attacks
# https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TZ', 'UTC')

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Manage templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '..', "web", "dist"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages"
            ],
        },
    },
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'api.middleware.APIVersionMiddleware',
]

ROOT_URLCONF = 'manager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'api.wsgi.application'

INSTALLED_APPS = (
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third-party apps
    'corsheaders',
    'guardian',
    'gunicorn',
    'rest_framework',
    'rest_framework.authtoken',
    'social_django',
    # manager apps
    'api',
)

AUTH_USER_MODEL = "api.User"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

GUARDIAN_GET_INIT_ANONYMOUS_USER = 'api.models.base.get_anonymous_user_instance'

LOGIN_URL = os.environ.get('LOGIN_URL', '/accounts/profile/')

# Security settings
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'Access-Control-Allow-Origin',
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'content-type',
    'accept',
    'origin',
    'Authorization',
    'Host',
    'user-agent',
    'X-CSRFToken',
    'DRYCC_API_VERSION',
    'DRYCC_PLATFORM_VERSION',
)
CORS_EXPOSE_HEADERS = (
    'DRYCC_API_VERSION',
    'DRYCC_PLATFORM_VERSION',
)

X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = None
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', None)
SESSION_COOKIE_SECURE = bool(strtobool(os.environ.get('SESSION_COOKIE_SECURE', 'false')))
CSRF_COOKIE_SECURE = bool(strtobool(os.environ.get('CSRF_COOKIE_SECURE', 'false')))

# Honor HTTPS from a trusted proxy
# see https://docs.djangoproject.com/en/2.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# standard datetime format used for logging, model timestamps, etc.
DRYCC_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
# django admin datetime format
DATETIME_FORMAT = "Y-m-d H:i:s e"

REST_FRAMEWORK = {
    'DATETIME_FORMAT': DRYCC_DATETIME_FORMAT,
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.ModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.DryccOIDCAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 30,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler'
}

# URLs that end with slashes are ugly
APPEND_SLASH = False

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'DEBUG' if DEBUG else 'WARN'},
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'filters': ['require_debug_true'],
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'propagate': True,
        },
        'api': {
            'handlers': ['console'],
            'propagate': True,
        },
        'registry': {
            'handlers': ['console'],
            'propagate': True,
        },
        'scheduler': {
            'handlers': ['console'],
            'propagate': True,
        },
    }
}

# security keys and auth tokens
random_secret = ')u_jckp95wule8#8wxdsm!0tj2j&aveozu!nnpgl)2x&&16gfj'
SECRET_KEY = os.environ.get('DRYCC_SECRET_KEY', random_secret)

# database setting
DRYCC_DATABASE_URL = os.environ.get('DRYCC_DATABASE_URL', 'postgres://:@:5432/manager')
DATABASES = {
    'default': dj_database_url.config(default=DRYCC_DATABASE_URL)
}

DRYCC_DATABASE_REPLICA_URL = os.environ.get('DRYCC_DATABASE_REPLICA_URL', None)
if DRYCC_DATABASE_REPLICA_URL is not None:
    DATABASES["replica"] = dj_database_url.config(default=DRYCC_DATABASE_REPLICA_URL)

# database routers
DATABASE_ROUTERS = ['api.routers.DefaultReplicaRouter', ]

# Redis Configuration
DRYCC_REDIS_ADDRS = os.environ.get('DRYCC_REDIS_ADDRS', '127.0.0.1:6379').split(",")
DRYCC_REDIS_PASSWORD = os.environ.get('DRYCC_REDIS_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'web', 'dist', 'assets'))
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Avatar URL
AVATAR_URL = "http://drycc-mirrors.drycc.cc/avatar/"
OAUTH_ENABLE = bool(strtobool(os.environ.get('OAUTH_ENABLE', 'true')))
if OAUTH_ENABLE:
    DRYCC_PASSPORT_URL = os.environ.get('DRYCC_PASSPORT_URL', 'https://127.0.0.1:8000')
    SOCIAL_AUTH_DRYCC_KEY = os.environ.get(
        'DRYCC_PASSPORT_KEY',
        os.environ.get('SOCIAL_AUTH_DRYCC_KEY'),
    )
    SOCIAL_AUTH_DRYCC_SECRET = os.environ.get(
        'DRYCC_PASSPORT_SECRET',
        os.environ.get('DRYCC_PASSPORT_SECRET'),
    )
    SOCIAL_AUTH_DRYCC_AUTHORIZATION_URL = os.environ.get(
        'SOCIAL_AUTH_DRYCC_AUTHORIZATION_URL',
        f'{DRYCC_PASSPORT_URL}/oauth/authorize/',
    )
    SOCIAL_AUTH_DRYCC_ACCESS_TOKEN_URL = os.environ.get(
        'SOCIAL_AUTH_DRYCC_ACCESS_TOKEN_URL',
        f'{DRYCC_PASSPORT_URL}/oauth/token/'
    )
    SOCIAL_AUTH_DRYCC_ACCESS_API_URL = os.environ.get(
        'SOCIAL_AUTH_DRYCC_ACCESS_API_URL',
        f'{DRYCC_PASSPORT_URL}/users/'
    )
    SOCIAL_AUTH_DRYCC_USERINFO_URL = os.environ.get(
        'SOCIAL_AUTH_DRYCC_ACCESS_TOKEN_URL',
        f'{DRYCC_PASSPORT_URL}/oauth/userinfo/'
    )
    SOCIAL_AUTH_DRYCC_JWKS_URI = os.environ.get(
        'SOCIAL_AUTH_DRYCC_JWKS_URI',
        f'{DRYCC_PASSPORT_URL}/oauth/.well-known/jwks.json'
    )
    SOCIAL_AUTH_DRYCC_OIDC_ENDPOINT = os.environ.get(
        'SOCIAL_AUTH_DRYCC_OIDC_ENDPOINT',
        f'{DRYCC_PASSPORT_URL}/oauth'
    )
    SOCIAL_AUTH_JSONFIELD_ENABLED = True
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.social_auth.associate_by_email',
        'api.pipeline.update_or_create',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )
    SOCIAL_AUTH_DISCONNECT_PIPELINE = (
        'social_core.pipeline.disconnect.get_entries',
        'social_core.pipeline.disconnect.revoke_tokens',
        'social_core.pipeline.disconnect.disconnect'
    )

    AUTHENTICATION_BACKENDS = ("api.backend.DryccOIDC", ) + AUTHENTICATION_BACKENDS

    OAUTH_CACHE_USER_TIME = int(os.environ.get('OAUTH_CACHE_USER_TIME', 30 * 60))

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
