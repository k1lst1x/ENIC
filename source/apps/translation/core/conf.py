"""
Языковая конфигурация веб-приложения.

Все операции и проверки выполняются на основе кода языка (lang_code),
например: 'ru', 'en', 'kk'. Названия языков (name) используются только
для отображения в пользовательском интерфейсе.
"""

# === Основные параметры поведения ===

ENABLE_DJANGO_TRANSLATION_ACTIVATE: bool = False  # Разрешить вызов django.utils.translation.activate(lang_code)
TRANSLATION_CACHE_TTL_SECONDS: int = 60 * 25     # Время жизни перевода в кэше (в секундах)

# === Языковые роли ===

DEFAULT_LANGUAGE_STARTUP: str = "kk"             # Язык, используемый по умолчанию при старте
TEMPLATE_LANGUAGE_REFERENCE: str = "ru"          # Язык, используемый как ключ в шаблонах и БД

# === Пути, исключённые из языкового редиректа ===

LANGUAGE_EXCLUDED_URL_PREFIXES: list[str] = [
    "/api/",     # API-интерфейс
    "/static/",  # Статические файлы
    "/media/",   # Медиафайлы (загрузка и отдача)
    "/uploads/",   # Медиафайлы (загрузка и отдача)
    "/admin/"

]

# === Список поддерживаемых языков ===

SUPPORTED_LANGUAGES: list[dict[str, str | bool]] = [
    {"code": "ru", "name": "Русский", "visible_in_ui": True},
    {"code": "en", "name": "English", "visible_in_ui": True},
    {"code": "kk", "name": "Қазақша", "visible_in_ui": True},
]

# === Публичные функции доступа ===

def get_supported_language_codes() -> list[str]:
    """
    Возвращает список поддерживаемых кодов языков, например: ['ru', 'en', 'kk'].
    """
    return [lang["code"] for lang in SUPPORTED_LANGUAGES]

def get_visible_languages() -> list[dict[str, str]]:
    """
    Возвращает список языков для отображения в UI.
    Пример: [{'code': 'ru', 'name': 'Русский'}, ...]
    """
    return [
        {"code": lang["code"], "name": lang["name"]}
        for lang in SUPPORTED_LANGUAGES
        if lang.get("visible_in_ui")
    ]

def get_language_name(lang_code: str) -> str:
    """
    Возвращает отображаемое название языка по его коду.
    Если код не найден, возвращает его как есть.
    """
    return next((lang["name"] for lang in SUPPORTED_LANGUAGES if lang["code"] == lang_code), lang_code)

# === Валидация конфигурации ===

def validate_translation_config() -> None:
    """
    Выполняет проверку конфигурации языков на корректность.

    Генерирует ValueError, если:
    - указанный язык старта или шаблонный язык не входят в SUPPORTED_LANGUAGES;
    - отсутствуют обязательные поля 'code' или 'name';
    - найдены дубликаты кодов языков;
    - путь-исключение не начинается с '/'.
    """
    codes = get_supported_language_codes()

    if DEFAULT_LANGUAGE_STARTUP not in codes:
        raise ValueError(
            f"DEFAULT_LANGUAGE_STARTUP ('{DEFAULT_LANGUAGE_STARTUP}') "
            f"не входит в SUPPORTED_LANGUAGES."
        )

    if TEMPLATE_LANGUAGE_REFERENCE not in codes:
        raise ValueError(
            f"TEMPLATE_LANGUAGE_REFERENCE ('{TEMPLATE_LANGUAGE_REFERENCE}') "
            f"не входит в SUPPORTED_LANGUAGES."
        )

    seen = set()
    for lang in SUPPORTED_LANGUAGES:
        code = lang.get("code")
        name = lang.get("name")
        if not code or not name:
            raise ValueError(f"Каждый язык обязан иметь 'code' и 'name'. Ошибка: {lang}")
        if code in seen:
            raise ValueError(f"Обнаружен дублирующий lang_code: '{code}'")
        seen.add(code)

    for path in LANGUAGE_EXCLUDED_URL_PREFIXES:
        if not path.startswith("/"):
            raise ValueError(
                f"Все значения LANGUAGE_EXCLUDED_URL_PREFIXES должны начинаться с '/'. "
                f"Нарушение: '{path}'"
            )

# === Автоматическая проверка при загрузке модуля ===

validate_translation_config()
