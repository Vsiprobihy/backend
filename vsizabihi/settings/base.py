import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed apps
    'djoser',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'social_django',

    # my app
    'authentication',
    'custom_admin',
    'organization',
    'user',
    'event',
    'public_event',
    'event.distance_details',
    'event.additional_items',
    'event.age_category',
    'event.promo_code',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'vsizabihi.middleware.DisableCSRF',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'vsizabihi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'vsizabihi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'authentication.authentication_backends.CustomAuthBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/authentication/userinfo.email',
    'https://www.googleapis.com/authentication/userinfo.profile',
    'openid',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
LOGIN_REDIRECT_URL = '/authentication/oauth/login-success/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'authentication.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For Gmail
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_ADMIN = os.getenv('GMAIL_ADMIN')
# EMAIL_SERVER = os.getenv('GMAIL_SERVER')
# EMAIL_HOST = os.getenv('GMAIL_HOST')
# EMAIL_PORT = os.getenv('GMAIL_PORT')
# EMAIL_HOST_USER = os.getenv('GMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('GMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_STARTTLS = True
# EMAIL_USE_SSL = False
# EMAIL_USE_TLS = True

DJOSER = {
    'SEND_ACTIVATION_EMAIL': True,
    'EMAIL': {
        'activation': 'authentication.emails.CustomActivationEmail',
        'password_reset': 'authentication.emails.CustomPasswordResetEmail',
        'password_changed_confirmation': 'authentication.emails.CustomPasswordChangedConfirmationEmail',
    },

    'PASSWORD_RESET_CONFIRM_URL': 'api/authentication/reset_password_confirm/{uid}/{token}/',
    'ACTIVATION_URL': 'api/authentication/activate/{uid}/{token}/',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

MAIN_PAGE_START_DATE_DAYS_AHEAD = (
    1  # Количество дней для начальной даты (для ендпоинта upcoming-events)
)
MAIN_PAGE_EVENT_DAYS_AHEAD = (
    5  # Количество дней, до которого отображаем события (для ендпоинта upcoming-events)
)

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {your JWT token}"',
        }
    },
}
