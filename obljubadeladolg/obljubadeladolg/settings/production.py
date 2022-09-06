from .base import *

DEBUG = bool(os.getenv('DJANGO_DEBUG', False))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DATABASE_NAME', 'wagtail'),
        'USER': os.getenv('DJANGO_DATABASE_USERNAME', 'wagtail'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD', 'changeme'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST', 'db'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', '5432'),
    }
}

# generate with
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'thisshouldbesecret')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', '/static/')
STATIC_URL = os.getenv('DJANGO_STATIC_URL_BASE', '/static/')


# S3 Storage
# DJANGO STORAGE SETTINGS
if os.getenv('DJANGO_ENABLE_S3', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID', '<TODO>')
    AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY', '<TODO>')
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME', 'djnd')
    AWS_DEFAULT_ACL = 'public-read' # if files are not public they won't show up for end users
    AWS_QUERYSTRING_AUTH = False # query strings expire and don't play nice with the cache
    AWS_LOCATION = os.getenv('DJANGO_AWS_LOCATION', 'obljubadeladolg')
    AWS_S3_REGION_NAME = os.getenv('DJANGO_AWS_REGION_NAME', 'fr-par')
    AWS_S3_ENDPOINT_URL = os.getenv('DJANGO_AWS_S3_ENDPOINT_URL', 'https://s3.fr-par.scw.cloud')
    AWS_S3_SIGNATURE_VERSION = os.getenv('DJANGO_AWS_S3_SIGNATURE_VERSION', 's3v4')

# --------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/app/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
