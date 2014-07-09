"""
Django settings for onboarding project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_z#g*3rkwob4yi+^5_w2&7h(z9hb1(x$_@6!+hqwq+(j6e=*%8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'signup',
    'bank_approvals',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'onboarding.urls'

WSGI_APPLICATION = 'onboarding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'NAME': 'merchants',
	'USER' : 'root',
	'PASSWORD': 'citrus',
	'HOST': 'localhost',
	'PORT': '3306',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
AUTH_PROFILE_MODULE = 'signup.Merchant'

TEMPLATE_DIRS = ( 
    os.path.join('./signup/', "templates"),
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.citruspay.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'bank-relations@citruspay.com'
EMAIL_HOST_PASSWORD = 'XzoTeGy7'
#EMAIL_HOST_PASSWORD = 'mppqtscylobmthab'
DEFAULT_FROM_EMAIL = 'vasughatole@gmail.com'
DEFAULT_TO_EMAIL = 'utkarsh.dixit11@gmail.com'
