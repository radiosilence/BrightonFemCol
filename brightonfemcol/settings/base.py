import django.conf.global_settings as DEFAULT_SETTINGS
import os, sys
from unipath import Path
# Django settings for brightonfemcol project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
APP = 'brightonfemcol'
SITE_DOMAIN = 'www.brightonfeministcollective.org.uk'
PREPEND_WWW = True
PROJECT_ROOT = Path(__file__).ancestor(3)

GRAPPELLI_ADMIN_TITLE = 'Brighton Feminist Collective'

ADMINS = (
    ('James Cleveland', 'james@dapperdogstudios.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'brightonfemcol',                      # Or path to database file if using sqlite3.
        'USER': 'brightonfemcol',                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': 'localhost:11211',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {  # Maps to pylibmc "behaviors"
            'tcp_nodelay': True,
            'ketama': True
        },
        'KEY_PREFIX': APP,
        'JOHNNY_CACHE': True,
    }
}

JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_{}'.format(APP)
JIMMY_PAGE_CACHE_PREFIX = "jp_{}".format(APP)

THUMBNAIL_QUALITY = 100
THUMBNAIL_COLORSPACE = None
THUMBNAIL_FORMAT = 'PNG'

DEFAULT_IMAGE = 'default-image.png'

ICON_PATH = 'images/mimetypes/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


STATIC_ROOT = PROJECT_ROOT.child('static')

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    '{0}.context_processors.{0}'.format(APP),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'require.storage.OptimizedCachedStaticFilesStorage'

REQUIRE_BASE_URL = "js"
REQUIRE_BUILD_PROFILE = 'default.build.js'
REQUIRE_JS = "require.js"
REQUIRE_DEBUG = DEBUG
REQUIRE_ENVIRONMENT = 'node'
REQUIRE_STANDALONE_MODULES = {
    "main": {
        # Where to output the built module, relative to REQUIRE_BASE_URL.
        "out": "main-built.js",

        # Optional: A build profile used to build this standalone module.
        "build_profile": "main.build.js",
    }
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# django-secure settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Disqus
DISQUS_API_KEY = os.environ.get('DJANGO_DISQUS_API_KEY')
DISQUS_WEBSITE_SHORTNAME = 'brightonfeministcollective'

ROOT_URLCONF = '{0}.urls'.format(APP)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{0}.wsgi.application'.format(APP)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    APP,
    'grappelli',
    'mptt',
    'require',
    'reversion',
    'south',
    'suave_press',
    'suave_calendar',
    'suave_discussion',
    'suave',
    'tinymce',
    'django_extensions',
    'sorl.thumbnail',
    'jimmypage',
    'djangosecure',
    'disqus',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.persona',
    'allauth.socialaccount.providers.twitter',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
)

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

