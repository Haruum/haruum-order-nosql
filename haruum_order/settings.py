"""
Django settings for haruum_order project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
from pymongo import MongoClient
import dj_database_url
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-kdp$qlc=09)l)ze38+e08p@)_@13f09$9*hr@#@fhvz@%2$ao#')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',

    'order',
    'review',
    'status',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'haruum_order.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'haruum_order.exception_config.custom_exception_handler',
}

WSGI_APPLICATION = 'haruum_order.wsgi.application'

# Database Settings
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')

MONGO_URL = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}'
MONGO_CLIENT = MongoClient(MONGO_URL)
DATABASE = MONGO_CLIENT[MONGO_DBNAME]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OUTLET_APPLICATION_URL = f"http://{os.getenv('OUTLET_APPLICATION_URL')}"
OUTLET_SERVICE_CATEGORIES_URL = f'{OUTLET_APPLICATION_URL}/search/outlet/services/?email='
OUTLET_ORDER_REGISTRATION_URL = f'{OUTLET_APPLICATION_URL}/order/create/'
OUTLET_ORDER_COMPLETION_URL = f'{OUTLET_APPLICATION_URL}/order/complete/'
OUTLET_RATING_UPDATE_URL = f'{OUTLET_APPLICATION_URL}/order/rating/'
OUTLET_GET_DATA_URL = f'{OUTLET_APPLICATION_URL}/user/data/?email='

CUSTOMER_APPLICATION_URL = f"http://{os.getenv('CUSTOMER_APPLICATION_URL')}"
CUSTOMER_CHECK_EXISTENCE_URL = f'{CUSTOMER_APPLICATION_URL}/user/check-exist/?email='
