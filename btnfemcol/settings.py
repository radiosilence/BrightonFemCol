# Default Configuration
DEBUG = False
SECRET_KEY = ''
LOG_LOCATION = 'error.log'
UPLOADED_AVATARS_DEST = 'btnfemcol/static/img/avatar'
UPLOADED_IMAGES_DEST = 'btnfemcol/static/img/event'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Get a key from http://code.google.com/apis/maps/signup.html
GMAPS_KEY = ''
STATIC_PATH = '/'

CACHE_TYPE = 'btnfemcol.utils.cache_pylibmc'
CACHE_KEY_PREFIX = 'btnfemcol'

CACHE_MEMCACHED_SERVERS = ['127.0.0.1']
CACHE_MEMCACHED_BINARY = True
CACHE_MEMCACHED_BEHAVIORS = {
    "tcp_nodelay": True,
    "ketama": True
}

try:
    from btnfemcol.local_settings import *
except ImportError:
    pass