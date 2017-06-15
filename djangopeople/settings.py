import dj_database_url
import os

from django.urls import reverse_lazy
from django.utils.six.moves.urllib import parse

OUR_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG = bool(os.environ.get('DEBUG', False))

# OpenID settings
OPENID_REDIRECT_NEXT = reverse_lazy('openid_whatnext')
LOGIN_URL = reverse_lazy('login')

# Tagging settings
FORCE_LOWERCASE_TAGS = True

ADMINS = MANAGERS = ()

DATABASES = {'default': dj_database_url.config()}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


def gettext(s):
    return s


LANGUAGES = (
    ('cs', gettext('Czech')),
    ('el', gettext('Greek')),
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
    ('fa', gettext('Persian')),
    ('fr', gettext('French')),
    ('he', gettext('Hebrew')),
    ('hi', gettext('Hindi')),
    ('id', gettext('Indonesian')),
    ('it', gettext('Italian')),
    ('pl', gettext('Polish')),
    ('pt', gettext('Portuguese')),
    ('pt_BR', gettext('Brazilian Portuguese')),
    ('ru', gettext('Russian')),
    ('sk', gettext('Slovak')),
    ('sq', gettext('Albanian')),
    ('sv', gettext('Swedish')),
    ('tr', gettext('Turkish')),
)

LOCALE_PATHS = (
    os.path.join(OUR_ROOT, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory where static media will be collected.
STATIC_ROOT = os.path.join(OUR_ROOT, 'static')

SECRET_KEY = os.environ['SECRET_KEY']

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Password used by the IRC bot for the API
API_PASSWORD = os.environ['API_PASSWORD']

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'builtins': [
            'django.templatetags.i18n',
        ],
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'sekizai.context_processors.sekizai',
        ],
    },
}]

if not DEBUG:
    # Use the cached template loader.
    del TEMPLATES[0]['APP_DIRS']
    TEMPLATES[0]['OPTIONS']['loaders'] = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangopeople.djangopeople.middleware.CanonicalDomainMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangopeople.djangopeople.middleware.RemoveWWW',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangopeople.django_openidconsumer.middleware.OpenIDMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'djangopeople.djangopeople.middleware.NoDoubleSlashes',
]

ROOT_URLCONF = 'djangopeople.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'tagging',

    'djangopeople.django_openidconsumer',
    'djangopeople.django_openidauth',
    'djangopeople.djangopeople',
    'djangopeople.machinetags',

    'password_reset',
    'sekizai',
]

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {'dsn': os.environ['SENTRY_DSN']}

GEONAMES_USERNAME = os.environ.get('GEONAMES_USERNAME', 'brutasse')

if 'CANONICAL_HOSTNAME' in os.environ:
    CANONICAL_HOSTNAME = os.environ['CANONICAL_HOSTNAME']
    ALLOWED_HOSTS = [CANONICAL_HOSTNAME]

SERVER_EMAIL = DEFAULT_FROM_EMAIL = os.environ['FROM_EMAIL']

SESSION_SERIALIZER = 'djangopeople.serializers.JSONSerializer'
X_FRAME_OPTIONS = 'DENY'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = ['127.0.0.1']
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )
else:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY']
    AWS_DEFAULT_ACL = 'public-read'
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
    AWS_QUERYSTRING_AUTH = False
    STATICFILES_STORAGE = 'djangopeople.s3storage.S3HashedFilesStorage'
    STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

    # Run the site over SSL
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 2592000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if 'REDISTOGO_URL' in os.environ:
    redis_url = parse.urlparse(os.environ['REDISTOGO_URL'])
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '{0}:{1}'.format(redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'DB': 0,
                'PASSWORD': redis_url.password,
            },
            'VERSION': os.environ.get('CACHE_VERSION', 0),
        },
    }
