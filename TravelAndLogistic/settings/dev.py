
from .base import *


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 30,
        'KEY_PREFIX': "dev"
    }
}

BROKER_URL =  'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND =  'redis://127.0.0.1:6379/1'

#DEBUG = config('DEBUG', False, cast=bool)
DEBUG = True