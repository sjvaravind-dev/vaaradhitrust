"""
Vaaradhi Trust — production-ready Django settings.
Tuned for ~20k–30k concurrent-friendly request handling via caching,
compressed static assets, and connection-friendly defaults.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "vaaradhi-dev-only-change-me-in-production-8f3k2m9x",
)

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

_raw_hosts = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,vaaradhi.gayatritechsolutions.com,"
    "vaaradhi.gayatritechsolutions.com,.gayatritechsolutions.com,"
    "gayatritechsolutions.com,www.gayatritechsolutions.com,"
    ".vaaradhi.org.in,vaaradhi.org.in,www.vaaradhi.org.in",
)
if _raw_hosts.strip() == "*":
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]
    for extra in (
        "localhost",
        "127.0.0.1",
        "vaaradhi.gayatritechsolutions.com",
        ".gayatritechsolutions.com",
        "gayatritechsolutions.com",
        "www.gayatritechsolutions.com",
        ".vaaradhi.org.in",
        "vaaradhi.org.in",
        "www.vaaradhi.org.in",
    ):
        if extra not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(extra)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "core.apps.CoreConfig",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "core.middleware.SiteTrafficMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_globals",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", str(BASE_DIR / "db.sqlite3")),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
        "OPTIONS": {"timeout": 30} if "sqlite" in os.getenv("DB_ENGINE", "sqlite") else {},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedStaticFilesStorage"
        ),
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Cache: Redis in production, LocMem for local ---
REDIS_URL = os.getenv("REDIS_URL", "")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {"max_connections": 100},
                "IGNORE_EXCEPTIONS": True,
            },
            "KEY_PREFIX": "vaaradhi",
            "TIMEOUT": 300,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "vaaradhi-cache",
            "TIMEOUT": 300,
            "OPTIONS": {"MAX_ENTRIES": 5000},
        }
    }

# Cache public pages aggressively for traffic spikes
CACHE_MIDDLEWARE_SECONDS = 120
CACHE_MIDDLEWARE_KEY_PREFIX = "vaaradhi_page"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "2000/hour",
        "user": "5000/hour",
    },
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "https://vaaradhi.gayatritechsolutions.com,https://gayatritechsolutions.com,https://www.gayatritechsolutions.com,https://vaaradhi.org.in,https://www.vaaradhi.org.in",
    ).split(",")
    if o.strip()
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://[\w.-]+\.vaaradhi\.org\.in$",
    r"^http://[\w.-]+\.vaaradhi\.org\.in$",
    r"^https://vaaradhi\.org\.in$",
    r"^http://vaaradhi\.org\.in$",
    r"^https://[\w.-]+\.gayatritechsolutions\.com$",
    r"^http://[\w.-]+\.gayatritechsolutions\.com$",
    r"^https://gayatritechsolutions\.com$",
    r"^http://gayatritechsolutions\.com$",
]
_csrf_default = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://vaaradhi.org.in",
    "https://www.vaaradhi.org.in",
    "http://vaaradhi.org.in",
    "http://www.vaaradhi.org.in",
    "https://*.vaaradhi.org.in",
    "http://*.vaaradhi.org.in",
    "https://vaaradhi.gayatritechsolutions.com",
    "https://*.gayatritechsolutions.com",
    "http://*.gayatritechsolutions.com",
    "https://gayatritechsolutions.com",
    "https://www.gayatritechsolutions.com",
]
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv("CSRF_TRUSTED_ORIGINS", ",".join(_csrf_default)).split(",")
    if o.strip()
]
# Auto-trust hosts from ALLOWED_HOSTS so subdomain and main domain both work.
if ALLOWED_HOSTS != ["*"]:
    for host in ALLOWED_HOSTS:
        for scheme in ("https://", "http://"):
            if host.startswith("."):
                origin = f"{scheme}*{host}"
            else:
                origin = f"{scheme}{host}"
            if origin not in CSRF_TRUSTED_ORIGINS:
                CSRF_TRUSTED_ORIGINS.append(origin)

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False").lower() in (
        "1",
        "true",
        "yes",
    )
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in (
        "1",
        "true",
        "yes",
    )
    CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() in (
        "1",
        "true",
        "yes",
    )
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

WHITENOISE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days
USE_X_FORWARDED_HOST = True
for _dir in (BASE_DIR / "logs", BASE_DIR / "media", BASE_DIR / "staticfiles"):
    try:
        _dir.mkdir(exist_ok=True)
    except OSError:
        pass

SITE_NAME = "Vaaradhi Trust"
SITE_TAGLINE = "Bridging Communities With Care"
SITE_URL = os.getenv("SITE_URL", "https://vaaradhi.gayatritechsolutions.com")
DEFAULT_OG_IMAGE = "/static/img/og-default.jpg"

# Razorpay — add keys in .env when ready (leave blank until then)
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "").strip()
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "").strip()
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "").strip()
DONATION_MIN_AMOUNT = int(os.getenv("DONATION_MIN_AMOUNT", "100"))

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },
}
_log_file = BASE_DIR / "logs" / "django.log"
try:
    _log_file.parent.mkdir(exist_ok=True)
    LOGGING["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "filename": str(_log_file),
    }
    LOGGING["root"]["handlers"].append("file")
except OSError:
    pass
