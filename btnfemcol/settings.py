# Default Configuration
DEBUG = False
SECRET_KEY = ''
LOG_LOCATION = 'error.log'
UPLOADED_AVATARS_DEST = 'btnfemcol/static/img/avatar'
UPLOADED_IMAGES_DEST = 'btnfemcol/static/img/event'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

# Get a key from http://code.google.com/apis/maps/signup.html
GMAPS_KEY = ''
STATIC_PATH = '/'

try:
    from btnfemcol.local_settings import *
except ImportError:
    pass