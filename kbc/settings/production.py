from __future__ import absolute_import, unicode_literals
from decouple import config
from .base import *
import dj_database_url

DEBUG = False
DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'kbc.urls.py'

SECRET_KEY = config('prod_key')

ALLOWED_HOSTS = ['*', 'vercel.app']

RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
NOCAPTCHA = True


try:
    from .local import *
except ImportError:
    pass
