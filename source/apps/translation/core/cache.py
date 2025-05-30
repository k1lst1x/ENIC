"""
Локальный in-memory кэш переводов для системы мультиязычности.

🔒 Потокобезопасность:
Кэш реализован как обычный Python-словарь в памяти (_cache), но все операции чтения и записи
защищены через threading.Lock. Это важно, потому что Django может обрабатывать несколько запросов параллельно.

⏳ Время жизни (TTL):
Каждая запись в кэше живёт строго определённое время (TRANSLATION_CACHE_TTL_SECONDS), после чего удаляется при обращении.

🧠 Использование:
- Ключ кэша: (исходный_текст, lang_code)
- Значение: (переведённый_текст, время_истечения)
- Применяется в get_translate() для ускорения доступа к переводу
"""

import threading
import time

from .conf import TRANSLATION_CACHE_TTL_SECONDS

# Внутреннее хранилище кэша:
# (key, lang_code) → (translated_value, expires_at)
_cache: dict[tuple[str, str], tuple[str, float]] = {}

# Глобальный lock для потокобезопасности
_cache_lock = threading.Lock()


def get_from_cache(key: str, lang_code: str) -> str | None:
    """
    Возвращает переведённое значение из кэша, если оно ещё не истекло.

    :param key: строка на TEMPLATE_LANGUAGE_REFERENCE
    :param lang_code: язык перевода
    :return: перевод, либо None, если записи нет или она устарела
    """
    now = time.time()
    cache_key = (key, lang_code)

    with _cache_lock:
        item = _cache.get(cache_key)
        if not item:
            return None

        value, expires_at = item
        if now > expires_at:
            del _cache[cache_key]
            return None

        return value


def save_to_cache(key: str, lang_code: str, value: str) -> None:
    """
    Сохраняет строку в кэш с TTL.

    :param key: исходный текст
    :param lang_code: язык перевода
    :param value: переведённый результат
    """
    expires_at = time.time() + TRANSLATION_CACHE_TTL_SECONDS
    with _cache_lock:
        _cache[(key, lang_code)] = (value, expires_at)
