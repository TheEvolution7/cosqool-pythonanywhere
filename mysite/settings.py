"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rc^*w^w&6g9_(uvx#6s*bnt!w)l0rdi%!l7mv#y%uc&x%wo5pk"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://cosqool.up.railway.app"]
# FORM SUBMISSION
# Comment out the following line and place your railway URL, and your production URL in the array.
# CSRF_TRUSTED_ORIGINS = ["*"]

# Application definition

INSTALLED_APPS = [
    # "modeltranslation",
    "dashboards",
    "auth.apps.AuthConfig",
    # 'contents',
    "pages",
    "articles",
    "fields",
    "menus",
    # 'albums',
    "settings",
    "products",
    "plans",
    # 'billings',
    # 'analytics',
    # 'orders',
    "accounts",
    # 'payments',
    # 'checkouts',
    "frontend",
    "courses",
    # 'contacts',
    "subscriptions",
    # 'invoices',
    "notification",
    "rest_framework",
    "django_filters",
    "api",
    "core",
    "core.files",
    "polymorphic",
    "nested_admin",
    "sections",
    "lessons",
    "quizzes",
    # 'takes',
    "events",
    "score",
    "seo",
    "polymorphic_tree",
    "content",
    "testpreps",
    "mysite.apps.MyAdminConfig",
    # 'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rosetta",
    "widget_tweaks",
    "parler",
    "imagekit",
    "mptt",
    "ckeditor",
    "ckeditor_uploader",
    "haystack",
    "django_cleanup.apps.CleanupConfig",
    "django_prices",
    "django_countries",
    "django_measurement",
    "django_phonenumbers",
    "django.contrib.humanize",
    "notes",
    "reporterror",
    "playlists",
    # 'paypal.standard.pdt',
    # 'paypal.standard.ipn',
    # 'bootstrap5',
    "import_export",
    "records",
]
PAYPAL_IDENTITY_TOKEN = "Tsu6-cO2xYiyU1O60uq19990dqAUpqY55KDiwMUrtEsU5UaWEQozP4fhIYq"
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = "ericbear0602@mail.com"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mysite.context_processors.admin_log_context",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': "railway",
    #     'USER': "postgres",
    #     'PASSWORD': "bB24EB1A4aBEd5BGb1E1dA5bB52e42C3",
    #     'HOST': "roundhouse.proxy.rlwy.net",
    #     'PORT': "31390",
    # }
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(os.path.dirname(__file__), "whoosh_index"),
    },
    "autocomplete": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(os.path.dirname(__file__), "whoosh_index"),
        "STORAGE": "file",
        "POST_LIMIT": 128 * 1024 * 1024,
        "INCLUDE_SPELLING": True,
        "BATCH_SIZE": 100,
        "EXCLUDED_INDEXES": ["thirdpartyapp.search_indexes.BarIndex"],
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/


LANGUAGE_CODE = "ar"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

PARLER_DEFAULT_LANGUAGE_CODE = "ar"

LANGUAGES = (
    ("en", "EN"),
    ("ar", "AR"),
)

PARLER_LANGUAGES = {
    None: (
        {
            "code": "en",
        },
        {
            "code": "ar",
        },
    ),
    "default": {
        "fallbacks": ["en"],
        "hide_untranslated": False,
    },
}

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_CUSTOM_FIELDS = ("title",)
MODELTRANSLATION_AUTO_POPULATE = True
MODELTRANSLATION_TRANSLATION_FILES = ("courses.translation",)
LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR, "media")
CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        # 'width': '100%',
        # 'height': '100%',
        "mathJaxLib": "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS_HTML",
        "extraPlugins": ",".join(
            [
                "a11yhelp",
                "about",
                "adobeair",
                "ajax",
                "autoembed",
                "autogrow",
                "autolink",
                # 'bbcode',
                # 'clipboard',
                "codesnippet",
                "codesnippetgeshi",
                "colordialog",
                # 'devtools',
                "dialog",
                "div",
                # 'divarea',
                "docprops",
                "embed",
                "embedbase",
                "embedsemantic",
                "filetools",
                "find",
                # 'flash',
                "forms",
                "iframe",
                "iframedialog",
                "image",
                # 'image2',
                "language",
                "lineutils",
                "link",
                "liststyle",
                "magicline",
                "mathjax",
                "menubutton",
                "notification",
                "notificationaggregator",
                "pagebreak",
                "pastefromword",
                "placeholder",
                "preview",
                "scayt",
                "sharedspace",
                "showblocks",
                "smiley",
                "sourcedialog",
                "specialchar",
                "stylesheetparser",
                "table",
                "tableresize",
                "tabletools",
                "templates",
                "uicolor",
                # 'uploadimage',
                "uploadwidget",
                "widget",
                "wsc",
                "xml",
                "ckeditor_wiris",
            ]
        ),
    },
    "ckeditor": {
        "width": "100%",
        "height": 100,
    },
}

X_FRAME_OPTIONS = "SAMEORIGIN"

DEFAULT_DECIMAL_PLACES = 2
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3

DEFAULT_COUNTRY = "US"

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    # ],
    # "DEFAULT_RENDERER_CLASSES": [
    #     "rest_framework.renderers.TemplateHTMLRenderer",
    #     "rest_framework.renderers.JSONRenderer",
    # ],
    # 'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    # 'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    # "DEFAULT_FILTER_BACKENDS": [
    #     "django_filters.rest_framework.DjangoFilterBackend",
    #     "rest_framework.filters.OrderingFilter",
    #     "rest_framework.filters.SearchFilter",
    # ],
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


# from import_export.formats.base_formats import XLSX
# IMPORT_EXPORT_FORMATS = [XLSX]

# from import_export.formats.base_formats import CSV, XLSX
# IMPORT_FORMATS = [CSV, XLSX]

# from import_export.formats.base_formats import XLSX
# EXPORT_FORMATS = [XLSX]
