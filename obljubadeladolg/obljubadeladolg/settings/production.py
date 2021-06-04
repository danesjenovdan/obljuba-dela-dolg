from .base import *

DEBUG = False

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

#ALLOWED_HOSTS = ['pravna-mreza.si', 'www.pravna-mreza.si']
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', '/static/')
STATIC_URL = os.getenv('DJANGO_STATIC_URL_BASE', '/static/')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT', '/media/')
MEDIA_URL = os.getenv('DJANGO_MEDIA_URL_BASE', '/media/')

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
