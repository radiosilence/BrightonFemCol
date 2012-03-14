# Default Configuration
DEBUG = False
SECRET_KEY = ''
DOMAIN_NAME = 'www.brightonfeministcollective.org.uk'
LOG_LOCATION = 'error.log'
UPLOADED_AVATARS_DEST = 'btnfemcol/static/img/avatar'
UPLOADED_IMAGES_DEST = 'btnfemcol/static/img/event'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Get a key from http://code.google.com/apis/maps/signup.html
GMAPS_KEY = ''
STATIC_PATH = '/'

CACHE_TYPE = 'flask.ext.cache_pylibmc.pylibmc'
CACHE_KEY_PREFIX = 'btnfemcol'

CACHE_MEMCACHED_SERVERS = ['127.0.0.1']
CACHE_MEMCACHED_BINARY = True
CACHE_MEMCACHED_BEHAVIORS = {
    "tcp_nodelay": True,
    "ketama": True
}

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None

DEFAULT_MAIL_SENDER = ('Brighton Feminist Collective',
    'no-reply@brightonfeministcollective.org.uk')

try:
    from btnfemcol.local_settings import *
except ImportError:
    pass