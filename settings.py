# -*- coding: utf-8 -*-
# Django settings for satchmo project.
# This is a recommended base setting for further customization
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DJANGO_PROJECT = 'cheze'
DJANGO_SETTINGS_MODULE = 'cheze.settings'

ADMINS = (
     ('Dom', 'web@quinode.fr'),         # tuple (name, email) - important for error reports sending, if DEBUG is disabled.
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'fr-FR'

SITE_ID = 1

STATIC_ROOT = os.path.abspath(PROJECT_PATH + '/static_collected/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.abspath(PROJECT_PATH + '/media/')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static/')
# MEDIA_URL = "/static/"

# ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'tb%=#%^d7o^93^m$u%g+$z8d=^1#vtk&v2hzr$--4^7y6f^pxk'


import admin_tools
ADMIN_TOOLS_PATH = os.path.dirname(os.path.abspath(admin_tools.__file__))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_DIRS = (
    os.path.abspath(PROJECT_PATH + '/static/'),
    os.path.abspath(ADMIN_TOOLS_PATH + '/media/'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "threaded_multihost.middleware.ThreadLocalMiddleware",
    "satchmo_store.shop.SSLMiddleware.SSLRedirect",
    #"satchmo_ext.recentlist.middleware.RecentProductMiddleware",
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

#this is used to add additional config variables to each request
# NOTE: If you enable the recent_products context_processor, you MUST have the
# 'satchmo_ext.recentlist' app installed.
TEMPLATE_CONTEXT_PROCESSORS = ('satchmo_store.shop.context_processors.settings',
                               'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.debug',
                               'django.core.context_processors.i18n',
                               'django.core.context_processors.media',
                               'django.core.context_processors.static',
                               'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.request',
                               #'satchmo_ext.recentlist.context_processors.recent_products',
                               'cheze.context_processors.footer',
                               )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.abspath(PROJECT_PATH + '/templates/'),
)

AUTOCOMPLETE_MEDIA_PREFIX = '/static/autocomplete/media/'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.sites',
    'satchmo_store.shop',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'registration',
    'sorl.thumbnail',
    'keyedcache',
    'livesettings',
    'l10n',
    'satchmo_utils.thumbnail',
    'satchmo_store.contact',
    'tax',
    ##'tax.modules.no',
    ##'tax.modules.area',
    ##'tax.modules.percent',
    ##'shipping',
    #'satchmo_store.contact.supplier',
    #'shipping.modules.tiered',
    #'satchmo_ext.newsletter',
    #'satchmo_ext.recentlist',
    #'testimonials',         # dependency on  http://www.assembla.com/spaces/django-testimonials/
    'product',
    'product.modules.configurable',
    'product.modules.custom',
    #'product.modules.downloadable',
    #'product.modules.subscription',
    #'satchmo_ext.product_feeds',
    #'satchmo_ext.brand',
    ##'payment',
    ##'payment.modules.dummy',
    #'payment.modules.purchaseorder',
    #'payment.modules.giftcertificate',
    #'satchmo_ext.wishlist',
    #'satchmo_ext.upsell',
    #'satchmo_ext.productratings',
    'satchmo_ext.satchmo_toolbar',
    'satchmo_utils',
    #'shipping.modules.tieredquantity',
    #'satchmo_ext.tieredpricing',
    #'typogrify',            # dependency on  http://code.google.com/p/typogrify/
    #'debug_toolbar',
    'app_plugins',
    'localsite',
    'django_extensions',
    'tinymce',
    'south',
)

AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced", 
    'relative_urls': False,
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_buttons1': 'bold,italic,|,justifyleft,justifycenter,justifyright,|,bullist,numlist,|,link,unlink',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3': ''
    }

TINYMCE_JS_URL = os.path.join(STATIC_URL, "tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL + 'tiny_mce')


#### Satchmo unique variables ####
#from django.conf.urls.defaults import patterns, include
SATCHMO_SETTINGS = {
    'SHOP_BASE': '',
    'MULTISHOP': False,
    #'SHOP_URLS' : patterns('satchmo_store.shop.views',)
    'PRODUCT_SLUG': 'produit',
    'CATEGORY_SLUG': 'categorie',
    'MEASUREMENT_SYSTEM': 'metric',
    
}

L10N_SETTINGS = {
  'currency_formats': {
     'EURO': {'symbol': u'€', 'positive': u"%(val)0.2f €", 'negative': u"€(%(val)0.2f)",
               'decimal': ','},
  },
  'default_currency': 'EURO',
  'show_admin_translations': False,
  'allow_translation_choice': False,
}


SKIP_SOUTH_TESTS = True

SATCHMO_DIRNAME = PROJECT_PATH
    
gettext_noop = lambda s: s

LANGUAGE_CODE = 'fr-FR'
LANGUAGES = (
#   ('en', gettext_noop('English')),
   ('fr', gettext_noop('French')),
)

#These are used when loading the test data
SITE_NAME = "Cheze SAS"

#These are used when loading the test data
SITE_DOMAIN = "www.cheze.fr"

# not suitable for deployment, for testing only, for deployment strongly consider memcached.
CACHE_BACKEND = "locmem:///"
CACHE_TIMEOUT = 60 * 5
CACHE_PREFIX = "Z"

ACCOUNT_ACTIVATION_DAYS = 7

# #Configure logging
# LOGFILE = "satchmo.log"
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename=os.path.join(PROJECT_PATH,LOGFILE),
#                     filemode='w')
# 
# logging.getLogger('keyedcache').setLevel(logging.INFO)
# logging.getLogger('l10n').setLevel(logging.INFO)
# logging.info("Satchmo Started")

# Load the local settings
from local_settings import *
