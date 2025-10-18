from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Security & environment
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-insecure-secret-key-change-me')
# Default DEBUG to False in hosted environments; override locally with DEBUG=True
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Helper to parse comma-separated env variables safely
_def_hosts = '127.0.0.1,localhost'
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', _def_hosts).split(',') if h.strip()]
# Add Render-provided hostname automatically if present
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
# Also allow any *.onrender.com subdomain (Django supports leading dot for subdomains)
if '.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.onrender.com')

# CSRF trusted origins: from env plus hosts -> https://host
_env_csrf = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]
CSRF_TRUSTED_ORIGINS = list(_env_csrf)
for _h in ALLOWED_HOSTS:
    if _h and _h != '*' and not _h.startswith('.'):
        CSRF_TRUSTED_ORIGINS.append(f'https://{_h}')
# De-duplicate while preserving order
_seen = set()
CSRF_TRUSTED_ORIGINS = [x for x in CSRF_TRUSTED_ORIGINS if not (x in _seen or _seen.add(x))]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'cloudinary',              # ← Cloudinary core SDK
    'cloudinary_storage',      # ← Django storage backend for Cloudinary
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If a DATABASE_URL is provided (e.g., by Render/Railway), prefer it
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        default=os.environ['DATABASE_URL'],
        conn_max_age=600,
        ssl_require=True,
    )

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------
# Cloudinary configuration (MEDIA storage)
# Set CLOUDINARY_URL in your environment, e.g.:
# export CLOUDINARY_URL="cloudinary://<api_key>:<api_secret>@<cloud_name>"
# ------------------------------
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

# Use Cloudinary for uploaded media if credentials are provided
if CLOUDINARY_URL:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    # Optional: keep uploads under a folder prefix in your Cloudinary account
    CLOUDINARY_STORAGE = {
        'SECURE': True,
        'PREFIX': 'clothify-media',
    }

# When running in production, use WhiteNoise for static files
if not DEBUG:
    existing_storages = globals().get('STORAGES', {})
    STORAGES = {
        **existing_storages,
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'