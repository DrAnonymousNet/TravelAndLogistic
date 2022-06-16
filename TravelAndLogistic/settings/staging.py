from ctypes import cast
from .base import *


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('POSTGRES_NAME'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': 5432,
        }
    }

DEBUG = config('DEBUG', False, cast=bool)
ALLOWED_HOSTS +=[]