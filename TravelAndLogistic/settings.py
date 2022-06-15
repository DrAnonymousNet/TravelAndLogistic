"""
Django settings for cfehome project.

Generated by 'django-admin startproject' using Django 4.1a1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ

env = environ.Env()

environ.Env.read_env()

from doctest import FAIL_FAST
import os
from pathlib import Path
from datetime import datetime, timedelta
from pickle import TRUE
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Installed app
    'Travel',
   'account',
    #External Package
    'rest_framework',
    'rest_framework.authtoken',
     'rest_framework_simplejwt',
     'djoser',
     "django_filters",
     'drf_yasg',

]

MIDDLEWARE = [
     "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'Travel.middleware.GetCurrentUserMiddleware'
]

ROOT_URLCONF = 'TravelAndLogistic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TravelAndLogistic.wsgi.application'



# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "account.UserAccount"


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/"staticfiles"
# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # <--
        'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.TokenAuthentication'],
   ],
    
    "DEFAULT_PERMISSION_CLASSES":[
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
   'AUTH_HEADER_TYPES': ('JWT',),
}

DJOSER = {
    "SEND_ACTIVATION_EMAIL":False,
    "LOGIN_FIELD":"email",
    "SEND_CONFIRMATION_EMAIL":False,
    "USER_CREATE_PASSWORD_RETYPE":True,
    "PASSWORD_RESET_RETYPE":True,
    "USERNAME_RESET_CONFIRM_URL":"email/reset/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL":"password/reset/{uid}/{token}",
    "ACTIVATION_URL":"activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL":True,
    "SERIALIZERS": {
        "user_create":"account.serializers.UserCreateSerializer",
        "user":"account.serializers.UserCreateSerializer",
        "user_delete":'djoser.serializers.UserDeleteSerializer'
    }
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "haryournifemijt@gmail.com"
EMAIL_HOST_PASSWORD ="uogqxmepgnilevmg"
EMAIL_USE_TLS = True
