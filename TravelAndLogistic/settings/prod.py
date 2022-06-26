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
            'HOST': 'db',
            'PORT': 5432,
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config("REDIS_URL"),
        'TIMEOUT': 30,
        'KEY_PREFIX': "dev"
    }
}

BROKER_URL = config("REDIS_URL")
CELERY_RESULT_BACKEND = config("REDIS_URL")



DEBUG = config('DEBUG', False, cast=bool)
ALLOWED_HOSTS += ["gowithease.herokuapp.com","*"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 
#STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

django_heroku.settings(locals())