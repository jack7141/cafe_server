"""
Django settings for cafe_backend project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import json
import logging
import logging.config
import pathlib
import datetime

from unipath import Path
from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).ancestor(2)
ROOT_DIR = pathlib.Path(__file__).resolve(strict=True).parent.parent.parent
SETTINGS_DIR = BASE_DIR.child('settings')
APPS_DIR = ROOT_DIR / 'cafe_backend'
SITE_ID = 1

secret_file_path = os.path.join(SETTINGS_DIR, 'secrets.json')

with open(secret_file_path, encoding='utf-8') as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        # if secrets.get(setting, None) else
        return secrets.get(setting) if secrets.get(setting, None) \
            else (getattr(global_settings, setting) if hasattr(global_settings, setting) else eval(setting))

        # return secrets[setting] if secrets[setting] else eval(setting)
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret('SECRET_KEY')
SITE_ID = 1
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_admin_inline_paginator',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'encrypted_model_fields',
    'drf_yasg',
    'elasticapm.contrib.django',
    'api.bases.cafe'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'elasticapm.contrib.django.middleware.TracingMiddleware',
]

ROOT_URLCONF = 'cafe_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cafe_backend.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '50/second',
    },
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

ELASTIC_APM = {
    "SERVICE_NAME": "cafe_manager",
    "DEBUG": True,
    "CAPTURE_BODY": "transactions",
    'SERVER_URL': 'localhost',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EXPIRING_TOKEN_LIFESPAN = 60 * 30

LOG_DIR_PATH = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(LOG_DIR_PATH):
    os.mkdir(LOG_DIR_PATH)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.request': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(levelname)s %(asctime)s pid: %(process)d] %(message)s',
        }
    },
    'handlers': {
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': '172.30.1.1',
            'port': 50000,
            'version': 1,
            'message_type': 'django',
            'fqdn': True,
            'tags': ['django'],
        },
        'django.request': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'django.request',
            'filters': ['require_debug_true']
        },
        'django.server': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': "midnight",
            'backupCount': 0,
            'encoding': 'UTF-8',
            'formatter': 'django.request',
            'filename': 'logs/server.log'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'django.request',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['django.request', 'console', 'logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server', 'console', 'logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'common.db_routers': {
            'handlers': ['console', 'logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
    'USE_SESSION_AUTH': True,
    'DOC_EXPANSION': 'None',
    'DEEP_LINKING': True,
    'DEFAULT_MODEL_DEPTH': 1,
    'DISPLAY_OPERATION_ID': False,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True
}

APPEND_SLASH = True
DATABASE_ROUTERS = ("common.db_routers.MasterSlaveRouter",)
