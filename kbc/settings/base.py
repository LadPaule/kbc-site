import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# Application definition
INSTALLED_APPS = [
    'home',
    'search',
    'kbc',
    'blog',
    'admindashboard',
    'crispy_forms',
    'streams',

    'bootstrapform',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.typed_table_block',
    'wagtail.embeds',
    'wagtail_gallery',
    'wagtail.contrib.table_block',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtailaudioembed',
    'wagtail.core',
    'wagtail_embed_videos',
    'wagtailmedia',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'modelcluster',
    'taggit',
    'mjml',
    'embed_video',
    'newsletter',
    'birdsong',
    'wagtail.contrib.modeladmin',
    'django.contrib.sitemaps',
    'django_comments_xtd',
    'django_comments',
    'django_social_share',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'captcha',
    'wagtailcaptcha',
]


COMMENTS_APP = 'django_comments_xtd'


RECAPTCHA_PUBLIC_KEY = '6Lfq8TQfAAAAAMlLAFH0D6kFFLCb4zCqcTqcsYzN'
RECAPTCHA_PRIVATE_KEY = '6Lfq8TQfAAAAAOX154JRXbjiygB_NbNuYt6fiHKX'

SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WAGTAILEMBEDS_RESPONSIVE_HTML = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'paul'
EMAIL_HOST_PASSWORD = 'Onemelchizedec'

MJML_EXEC_CMD = './node_modules/.bin/mjml'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'kbc.urls'

WAGTAILMEDIA = {
    "AUDIO_EXTENSIONS": [ "aac", "aiff", "flac", "m4a", "m4b", "mp3", "ogg", "wav"],  # list of extensions
    "VIDEO_EXTENSIONS": ["avi", "h264", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg", "ogv", "webm"],  # list of extensions
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
LOGIN_URL='/login/'
LOGIN_REDIRECT_URL='/admin/'
ACCOUNT_AUTHENTICATION_METHOD='username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=7
ACCOUNT_CONFIRM_EMAIL_ON_GET=True
ACCOUNT_EMAIL_VERIFICATION='mandatory'
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT=300
ACCOUNT_SESSION_REMEMBER=True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT=5
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
CCOUNT_LOGOUT_ON_GET=True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE=True
ACCOUNT_LOGIN_ON_PASSWORD_RESET=False
ACCOUNT_LOGOUT_REDIRECT_URL='/'
ACCOUNT_PRESERVE_USERNAME_CASING=False
ACCOUNT_SESSION_REMEMBER=True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE=True
ACCOUNT_USERNAME_BLACKLIST=["admin", "root", "test","God", "Devil", "Admin", "Root", "Test"]
ACCOUNT_USERNAME_MIN_LENGTH=2

WSGI_APPLICATION = 'kbc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "Kampala Baptist Church"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

# Recaptcha settins

