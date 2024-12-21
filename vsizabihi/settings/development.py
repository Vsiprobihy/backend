from .base import *  # noqa


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

# from VADIM
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'probihy',
#         'USER': 'probihy',
#         'PASSWORD': 'probihy',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
