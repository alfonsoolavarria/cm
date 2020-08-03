"""
Django settings for market project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3(%m#=&3u)%dxq$#%8)&5+kyy3(5y0d9dt-f@lvj7!3cgv8$-e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #en prod False

ALLOWED_HOSTS = ['127.0.0.1','*'] #* en prod remove


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maracay',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'market.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+'/market/templates'],
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

WSGI_APPLICATION = 'market.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.db.backends.sqlite3',
        #'TIMEOUT':2,
        'NAME': 'criollitos',
        'USER': 'postgres',
        # 'PASSWORD': '21098026',
        'HOST': 'localhost',
        'PORT': '5432',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#####db de produccion
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
#####db de produccion



# DATABASES['default'] = dj_database_url.parse('postgres://wudwjeeqngsoln:db0b4d57a4280154798016702a4a2427d32691a5d00efd39e75468263be770a1@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d7rddbdt0sbmee', conn_max_age=600)
#https://fierce-garden-63252.herokuapp.com/
#'postgres://wudwjeeqngsoln:db0b4d57a4280154798016702a4a2427d32691a5d00efd39e75468263be770a1@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d7rddbdt0sbmee'
# DATABASES = {
#         'default': {
#             'ENGINE': 'djongo',
#             'ENFORCE_SCHEMA': True,
#             'NAME': 'criollotest',
#             'host': '127.0.0.1',
#             'port': 27017,
#             'username': 'root',
#             'password': 'root',
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
###########original
STATIC_URL = '/static/'
#
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT,'static')
STATICFILES_DIRS = (os.path.join(STATIC_ROOT, 'static'),)
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/images/upload')
MEDIA_URL = PROJECT_ROOT+'/static/images/upload/'
FILE_UPLOAD_PERMISSIONS = 0o777

##################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )


# EMAIL_BACKEND
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'criollitosmarket@gmail.com'
EMAIL_HOST_PASSWORD = 'udhdwnanhbgcwbzh'
EMAIL_PORT = 587
