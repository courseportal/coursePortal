# Django settings for knoatom-web project.
import os
from django.utils.crypto import get_random_string
# Function that generates secret keys
def generate_secret_key(filename):
    r"""Creates a file that defines a random SECRET_KEY in a file located at filename."""
    secret_key_file = open(filename, 'w')
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)
    secret_key_file.write('SECRET_KEY = "{}"'.format(secret_key))
    secret_key_file.close()

ADMINS = (
    ('Nick Terrell', 'terrelln@umich.edu'),
    ('Jacob Texel', 'texel@umich.edu'),
    ('Taoran Yan','tyan@umich.edu'),
)

MANAGERS = ADMINS

# For PYBB
PYBB_TEMPLATE = 'forum_base.html'
PYBB_POLL_MAX_ANSWERS = 10

# List of allowed file upload types
ALLOWED_FILE_EXTENSIONS = ['.pdf']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880"


FILE_UPLOAD_HANDLERS= ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                       "django.core.files.uploadhandler.TemporaryFileUploadHandler",)


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
                       'django.contrib.staticfiles.finders.FileSystemFinder',
                        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
                       )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    #     'django.template.loaders.eggs.Loader',
                    )

MIDDLEWARE_CLASSES = (
                      'django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'pybb.middleware.PybbMiddleware',
                      )

ROOT_URLCONF = 'knoatom.urls'

from os import path

TEMPLATE_DIRS = (
                 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
                 # Always use forward slashes, even on Windows.
                 # Don't forget to use absolute paths, not relative paths.
                 path.join(path.dirname(__file__), 'templates'),
                 )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'haystack',
    'rating',
    'knoatom',
    'web',
    'assignment',
    'django_wysiwyg',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # For PYBBM
    'pybb',
    'sorl.thumbnail',
    'autocomplete_light',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_URL = '/login'

HTTPS_SUPPORT = True
SECURE_REQUIRED_PATHS = (
    '/login',
    '/account',
    '/admin',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
}
}

TEMPLATE_CONTEXT_PROCESSORS = (
   "django.contrib.auth.context_processors.auth",
   "django.core.context_processors.debug",
   "django.core.context_processors.i18n",
   "django.core.context_processors.media",
   "django.core.context_processors.request",
   "django.core.context_processors.static",
   "django.core.context_processors.tz",
   "django.contrib.messages.context_processors.messages",
   "django.core.context_processors.csrf",
   'pybb.context_processors.processor',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        #'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
    #'BATCH_SIZE': 100,
    },
}


HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

#Default is 'AND', can also be changed to 'OR'
#HAYSTACK_DEFAULT_OPERATOR = 'AND'

#controls what fieldname Haystack relies on as the default field for searching within. Default='text'
#HAYSTACK_DOCUMENT_FIELD = 'text'
