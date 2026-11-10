from .base import *

DEBUG = bool(os.getenv("DJANGO_DEBUG", False))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DJANGO_DATABASE_NAME", "wagtail"),
        "USER": os.getenv("DJANGO_DATABASE_USERNAME", "wagtail"),
        "PASSWORD": os.getenv("DJANGO_DATABASE_PASSWORD", "changeme"),
        "HOST": os.getenv("DJANGO_DATABASE_HOST", "db"),
        "PORT": os.getenv("DJANGO_DATABASE_PORT", "5432"),
    }
}

# generate with
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "thisshouldbesecret")

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", "/static/")
STATIC_URL = os.getenv("DJANGO_STATIC_URL_BASE", "/static/")

ENABLE_S3 = os.getenv("DJANGO_ENABLE_S3", False)
# DJANGO STORAGE SETTINGS
if ENABLE_S3:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.getenv("DJANGO_AWS_ACCESS_KEY_ID", ""),
                "secret_key": os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY", ""),
                "bucket_name": os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME", ""),
                "region_name": os.getenv("AWS_REGION_NAME", "fr-par"),
                "endpoint_url": os.getenv(
                    "DJANGO_AWS_S3_ENDPOINT_URL", "https://s3.fr-par.scw.cloud"
                ),
                "location": os.getenv("DJANGO_AWS_LOCATION", "storyteller"),
                "file_overwrite": os.getenv("AWS_S3_FILE_OVERWRITE", False),
                "signature_version": os.getenv(
                    "DJANGO_AWS_S3_SIGNATURE_VERSION", "s3v4"
                ),
                "querystring_auth": os.getenv("AWS_QUERYSTRING_AUTH", False),
                "default_acl": os.getenv("AWS_DEFAULT_ACL", "public-read"),
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# --------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/app/debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
