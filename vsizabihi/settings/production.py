from .base import *  # noqa: F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'probihy_db',
        'USER': 'vsi_probihy_user',
        'PASSWORD': 'probihy_password',
        'HOST': 'data-base',
        'PORT': '5432',
    }
}
