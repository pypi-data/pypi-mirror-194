from texsite.application.config import PACKAGE_ROOT


BASE_DIR = PACKAGE_ROOT.parent

# Application definition
INSTALLED_APPS = [
    # texsite apps
    'texsite.businesscasual',
    'texsite.cleanblog',
    'texsite.core',
    # texperience apps
    'bootstrap_ui',
    # Third party apps
    'wagtailmenus',
    # Wagtail apps
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.redirects',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.admin',
    'wagtail.core',
    # Wagtail dependencies
    'modelcluster',
    'taggit',
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'texsite.application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PACKAGE_ROOT / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGES = (('de', 'Deutsch'),)
LANGUAGE_CODE = 'de'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Europe/Berlin'

# Static files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Wagtail settings
WAGTAIL_SITE_NAME = 'texsite'
PASSWORD_REQUIRED_TEMPLATE = 'texsitebusinesscasual/login_password.html'

# Wagtailmenus settings
WAGTAILMENUS_MAIN_MENUS_EDITABLE_IN_WAGTAILADMIN = False

# Base URL to use when referring to full URLs within the Wagtail admin backend,
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'
