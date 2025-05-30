"""
Управляет активным языковым контекстом для текущего потока выполнения.

 Принцип:
- Один язык (lang_code) назначается в начале обработки каждого запроса.
- Он сохраняется в потокобезопасное хранилище (threading.local), чтобы быть доступным в любой части кода.
- Это позволяет вызывать get_language() без передачи request или context.
"""

import threading
from .conf import get_supported_language_codes

# Локальное хранилище — изолировано на уровне потока (1 поток = 1 запрос)
_local = threading.local()

# Кэш допустимых языков (lang_code), полученных из конфигурации
_valid_codes = set(get_supported_language_codes())


def set_language(lang_code: str) -> None:
    """
    Устанавливает активный lang_code для текущего потока (запроса).
    
    Обычно вызывается в middleware после разбора URL.
    Этот язык используется везде в рамках одного запроса:
    - при get_translate()
    - при построении путей
    - в шаблонных тегах и контекстах

    :raises ValueError: если язык не входит в список SUPPORTED_LANGUAGES
    """
    if lang_code not in _valid_codes:
        raise ValueError(
            f"Недопустимый lang_code '{lang_code}'. Разрешены: {', '.join(sorted(_valid_codes))}"
        )
    _local.lang = lang_code


def get_language() -> str:
    """
    Возвращает текущий lang_code, установленный ранее через set_language().
    
    Этот метод безопасно вызывать из любого кода, где уже прошёл middleware.
    
    :raises RuntimeError: если set_language() ещё не был вызван
    """
    if hasattr(_local, "lang"):
        return _local.lang

    raise RuntimeError(
        "Языковой контекст не инициализирован. "
        "set_language(lang_code) должен быть вызван в начале обработки запроса."
    )
