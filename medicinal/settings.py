from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# SECURITY
# ================================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-key"
)

DEBUG = os.getenv("VERCEL") is None
DEBUG = False

ALLOWED_HOSTS = [
    ".vercel.app",
    "localhost",
    "127.0.0.1"
]


# ================================
# APPLICATIONS
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

    # WhiteNoise for static files on Vercel
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================================
# URLS & WSGI
# ================================
ROOT_URLCONF = 'medicinal.urls'

WSGI_APPLICATION = 'medicinal.wsgi.application'


# ================================
# TEMPLATES
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Your templates folder
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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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
# EMAIL
# ================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ================================
# LOGIN / LOGOUT
# ================================
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'index'


# ================================
# OPTIONAL ENV VARIABLES
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")

MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")

MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")

MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

MPESA_CALLBACK_URL = os.getenv(
    "MPESA_CALLBACK_URL",
    "https://your-app.vercel.app/mpesa/callback/"
)