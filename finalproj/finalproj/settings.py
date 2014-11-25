"""
Django settings for finalproj project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates/codebook/'),)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&qqui3j2oe&3mf!bg%h+ehr*2zl!ji)jj1wvi2w6w9egq6m1@s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'codebook',
    'social.apps.django_app.default',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.github.GithubOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

# these are the settings for local development
#SOCIAL_AUTH_GITHUB_KEY = '31fd927b2ac22678d050'
#SOCIAL_AUTH_GITHUB_SECRET = '431197c65d51dc0ae5e4919fc44a999b95e2fef3'

# new keys for deployment:
SOCIAL_AUTH_GITHUB_KEY = 'aca57928bf5933e6f19e'
SOCIAL_AUTH_GITHUB_SECRET = '477759c2ab4260dcb708c1c719a370d316891840'
SOCIAL_AUTH_GITHUB_SCOPE = ['repo']
SOCIAL_AUTH_USER_MODEL = 'codebook.ProfileUser'

ROOT_URLCONF = 'finalproj.urls'

WSGI_APPLICATION = 'finalproj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'codebook',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',    # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',             # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


ROOT_URLCONF = 'finalproj.urls'

LOGIN_URL = '/codebook/'

LOGIN_REDIRECT_URL = '/codebook/'

WSGI_APPLICATION = 'finalproj.wsgi.application'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/home/ubuntu/test_site.com/finalproj/codebook/static'

# Configures Django to merely print emails rather than sending them.
# Comment out this line to enable real email-sending.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# To enable real email-sending, you should uncomment and 
# configure the settings below.
# EMAIL_HOST = 'Your-SMTP-host'               # perhaps 'smtp.andrew.cmu.edu'
# EMAIL_HOST_USER = 'Your-SMTP-username'      # perhaps your Andrew ID
# EMAIL_HOST_PASSWORD = 'Your-SMTP-password'
# EMAIL_USE_TLS = True


DEBUG_TOOLBAR_PATCH_SETTINGS = False