
from pathlib import Path
import os

import django_heroku
import dj_database_url
from decouple import config
from dotenv import load_dotenv, find_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['www.cheekycv.com','cheekycv.com','cheekycv.herokuapp.com','localhost']

# SSL SETTINGS

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True


# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_RELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'user_auth',
    'storages',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cheekycv_new_1.urls'

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

WSGI_APPLICATION = 'cheekycv_new_1.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3',conn_max_age = 600)
}

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC_URL = '/static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'



#-------EMAIL SETTINGS----------------------------

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# AWS SETTINGS

AWS_ACCES_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCES_KEY = os.environ.get('AWS_SECRET_ACCES_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age-86400'}
AWS_LOCATION = 'static'
AWS_HEADERS = {
    'Access-Control-Allow-Origin':'*'
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
STATIC_URL = 'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = 'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


#HEROKU SETTINGS

django_on_heroku.settings(locals(), staticfiles = False)
del DATABASES['default']['OPTIONS']['sslmode']

#HEROKU LOGGING

DEBUG_PROPAGATE_EXCEPTIONS = True

LOGGING = {
    'version':1,
    'disable_existing_loggers': False,
    'formatters':{
        'verbose':{
            'format':'[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt':'%d/%b/%Y %H:%M:%S'


        },
        'simple':{
            'format':'%(levelname)s %(message)s'
        },
    },
    'handlers':{
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },

    },
    'loggers':{
        'app':{
            'handlers':['console'],
            'level':'DEBUG',
        },
    }
}


# #--------------------------
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR,"static"),
#     )
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# MEDIA_URL = '/img/'

# MEDIA_ROOT = os.path.join(BASE_DIR, "img")

# #------------------

# db_from_env = dj_database_url.config()
# DATABASES['default'].update(db_from_env)

# #--------------------------------------------------------------------
# DISABLE_COLLECTSTATIC = 1

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# django_heroku.settings(locals())