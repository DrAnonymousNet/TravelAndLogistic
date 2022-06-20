from ctypes import cast
from .base import *
import django_heroku

#h
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('POSTGRES_NAME'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': '',
            'PORT': 5432,
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 30,
        'KEY_PREFIX': "prod"
    }
}
'''
DEBUG = config('DEBUG', False, cast=bool)
ALLOWED_HOSTS += ["gowithease.herokuapp.com","*"]
STATICFILES_STORAGE = "whitenoise.storage.ManifestStaticFilesStorage"
#STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

django_heroku.settings(locals())