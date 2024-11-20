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
# include database sqlite3
# from .base import BASE_DIR
#
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
