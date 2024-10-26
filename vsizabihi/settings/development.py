from .base import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'probihy_db',
        'USER': 'vsi_probihy_user',
        'PASSWORD': 'probihy_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'