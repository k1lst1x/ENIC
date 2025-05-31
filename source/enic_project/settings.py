import os
from pathlib import Path
from dotenv import load_dotenv

# =============================
# Base Directory Configuration
# =============================

BASE_DIR = Path(__file__).resolve().parent.parent       # /enic/source
PROJECT_ROOT = BASE_DIR.parent                          # /enic
RUNTIME_DIR = PROJECT_ROOT / "runtime"                  # /enic/runtime

load_dotenv(PROJECT_ROOT / ".env")

# =============================
# Core Settings
# =============================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# =============================
# Security Settings
# =============================

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =============================
# Installed Applications
# =============================

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.translation",
    "apps.common",

    "django_ckeditor_5",
]

# =============================
# Middleware Stack
# =============================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.translation.middleware.CustomLocaleMiddleware",


]

# =============================
# URL & WSGI Configuration
# =============================

ROOT_URLCONF = "enic_project.urls"
WSGI_APPLICATION = "enic_project.wsgi.application"

# =============================
# Templates
# =============================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.translation.context_processors.current_language",
            ],
        },
    },
]

# =============================
# Database Configuration
# =============================

DATABASE_MODE = os.getenv("DATABASE_MODE", "sqlite")

if DATABASE_MODE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": RUNTIME_DIR / "db.sqlite3",
        }
    }
elif DATABASE_MODE == "psql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD"),
            "HOST": os.getenv("DATABASE_HOST", "localhost"),
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }
else:
    raise ValueError("Invalid DATABASE_MODE: must be 'sqlite' or 'psql'")

# =============================
# Caching
# =============================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache_table",
        "TIMEOUT": None,
        "OPTIONS": {"MAX_ENTRIES": 10000},
    }
}

# =============================
# Logging
# =============================

LOG_DIR = RUNTIME_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

MAX_LOG_SIZE = 15 * 1024 * 1024  # 15 MB
LOG_BACKUPS = 3

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(pathname)s:%(lineno)d\n%(message)s",
        },
        "simple": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "error_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "formatter": "verbose",
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": LOG_BACKUPS,
            "encoding": "utf-8",
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "info.log",
            "formatter": "simple",
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": LOG_BACKUPS,
            "encoding": "utf-8",
        },
        "django_console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "debug_mode_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["info_file", "error_file", "django_console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django_console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["info_file", "error_file", "debug_mode_console"],
        "level": "DEBUG",
    },
}

# =============================
# Password Validation
# =============================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================
# Localization
# =============================

LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True

# =============================
# Email Settings
# =============================

EMAIL_MODE = os.getenv("EMAIL_MODE", "console")

if EMAIL_MODE == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_MODE == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
else:
    raise ValueError("Invalid EMAIL_MODE: must be 'console' or 'smtp'")

# =============================
# Static & Media Files
# =============================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.getenv("STATIC_ROOT", RUNTIME_DIR / "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("MEDIA_ROOT", RUNTIME_DIR / "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

print(
    "\n[settings] Project loaded with the following configuration:\n"
    f" ├─ DEBUG:            {DEBUG}\n"
    f" ├─ DATABASE_MODE:    {DATABASE_MODE}\n"
    f" ├─ DATABASE_ENGINE:  {DATABASES['default']['ENGINE']}\n"
    f" ├─ EMAIL_MODE:       {EMAIL_MODE}\n"
    f" ├─ STATIC_ROOT:      {STATIC_ROOT}\n"
    f" ├─ MEDIA_ROOT:       {MEDIA_ROOT}\n"
    f" └─ ALLOWED_HOSTS:    {ALLOWED_HOSTS}\n"
)


JAZZMIN_SETTINGS = {
    # Основное
    "site_title": "НЦ РВО",  # Заголовок страницы браузера
    "site_header": "НАЦИОНАЛЬНЫЙ ЦЕНТР РАЗВИТИЯ ВЫСШЕГО ОБРАЗОВАНИЯ",  # Верхний заголовок панели
    "site_brand": "НЦ РВО",  # Название в логотипе
    "site_logo_classes": "img-circle",  # Классы оформления логотипа
    "site_logo_width": "64px",  # Ширина логотипа
    "site_logo_height": "64px",  # Высота логотипа
    "site_logo": "favicon-32x32.png",  # 🖼️ Логотип слева вверху
    "site_icon": "favicon-32x32.png",  # 🧷 Favicon на всех страницах (вкладка браузера, login и т.д.)
    "welcome_sign": "Добро пожаловать в панель НАЦИОНАЛЬНЫЙ ЦЕНТР РАЗВИТИЯ ВЫСШЕГО ОБРАЗОВАНИЯ",  # Приветствие на экране входа
    "copyright": "© 2025",  # Подпись в подвале
    "topmenu_links": [  # Верхнее меню
        {"name": "На сайт", "url": "/", "icon": "fas fa-globe"},
    ],
    "show_sidebar": True,  # Показывать ли боковое меню
    "navigation_expanded": True,  # Разворачивать ли меню по умолчанию
    "custom_css": "admin/custom.css",  # Кастомный файл для стилизации интерфейса
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # Цветовая тема интерфейса
    "dark_mode": True,  # Включение тёмного режима
}

# Settings for CKEditor

# CKEDITOR_5_FILE_STORAGE = "app.storage.CustomStorage"
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "language": "ru",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "codeBlock",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True},
            ]
        },
    },
}

CKEDITOR_5_UPLOAD_FILE_TYPES = [
    'jpeg',
    'jpg',
    'png',
    'gif',
    'bmp',
    'svg',
    'webp',
    'pdf',
    'doc',
    'docx',
    'xls',
    'xlsx',
]
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # Possible values: "staff", "authenticated", "any"
CKEDITOR_5_MAX_FILE_SIZE = 100
CKEDITOR_UPLOAD_PATH = "ckeditor5_uploads/"
CKEDITOR_5_FILE_STORAGE = "app.ckeditor.CKEditorStorage"
