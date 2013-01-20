from .base import *

import sys
import warnings

warnings.filterwarnings(
        'error', r"DateTimeField received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

DEBUG = True
COMPRESS_ENABLED = True
THUMBNAIL_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG
REQUIRE_DEBUG = DEBUG
PREPEND_WWW = False
ADMINS = (
    ('James Cleveland', 'jamescleveland@gmail.com'),
)
INTERNAL_IPS = ('127.0.0.1',)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#         'JOHNNY_CACHE': True,
#     }
# }

SESSION_ENGINE = 'django.contrib.sessions.models'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level':'DEBUG',
#             'class':'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     }
# }
# import logging
