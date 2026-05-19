from pathlib import Path
import os
from dotenv import load_dotenv

import dj_database_url




# ================================
# LOAD ENV VARIABLES
# ================================
load_dotenv()

# ================================
# BASE DIRECTORY
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ================================
# SECURITY
# ================================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-key"
)

# False on Vercel / production
DEBUG = os.getenv("VERCEL") is None

ALLOWED_HOSTS = [
    ".vercel.app",
    "localhost",
    "127.0.0.1",
]


# ================================
# INSTALLED APPLICATIONS
# ================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your app
    'medical',
]


# ================================
# MIDDLEWARE
# ================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================================
# ROOT URLS
# ================================
ROOT_URLCONF = 'medicinal.urls'


# ================================
# WSGI
# ================================
WSGI_APPLICATION = 'medicinal.wsgi.application'


# ================================
# TEMPLATES
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # templates folder
        'DIRS': [BASE_DIR / 'templates'],

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


# ================================
# DATABASE
# ================================






DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600
    )
}


# ================================
# PASSWORD VALIDATION
# ================================
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


# ================================
# INTERNATIONALIZATION
# ================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# ================================
# STATIC FILES
# ================================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# ================================
# MEDIA FILES
# ================================
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ================================
# DEFAULT PRIMARY KEY
# ================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================================
# EMAIL CONFIGURATION
# ================================
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")

EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ================================
# LOGIN / LOGOUT
# ================================
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'index'


# ================================
# OPENAI
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ================================
# MPESA
# ================================
MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")

MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")

MPESA_SHORTCODE = os.getenv(
    "MPESA_SHORTCODE",
    "174379"
)

MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

MPESA_CALLBACK_URL = os.getenv(
    "MPESA_CALLBACK_URL",
    "https://your-app.vercel.app/mpesa/callback/"
)


# ================================
# SECURITY HEADERS (PRODUCTION)
# ================================
if not DEBUG:

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = 'DENY'

    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True