"""
Интерфейс получения перевода строки для текущего языка.

Принцип работы:
Перевод осуществляется на основе активного lang_code (установленного через set_language).
Решение о том, что показывать, происходит строго в этом порядке:

1.Кэш: если перевод уже есть в оперативной памяти — возвращаем его мгновенно.
2.База данных: если в кэше нет — достаём из модели Translation (либо создаём новую запись).
3.Возврат оригинала: если перевод отсутствует, возвращаем исходную строку (обычно на TEMPLATE_LANGUAGE_REFERENCE).

Безопасность:
Если язык не установлен через set_language(), произойдёт RuntimeError.

Примечание:
Этот интерфейс работает независимо от gettext и встроенной системы Django i18n.
"""

import logging

from .active_language_context import get_language
from .cache import get_from_cache, save_to_cache
from .conf import TEMPLATE_LANGUAGE_REFERENCE
from ..models import Translation

logger = logging.getLogger("translation.translator")


def get_translate(key: str) -> str:
    """
    Возвращает переведённую строку на основе текущего языка.

    :param key: исходная строка на языке TEMPLATE_LANGUAGE_REFERENCE (обычно 'ru')
    :return: строка на активном lang_code или оригинал, если перевода нет
    """
    lang_code = get_language()

    # 0. Если активный язык — язык-ключ, то возвращаем сам ключ
    if lang_code == TEMPLATE_LANGUAGE_REFERENCE:
        return key

    # 1. Попытка взять из кэша
    cached = get_from_cache(key, lang_code)
    if cached:
        return cached

    # 2. Поиск в базе данных (или создание записи)
    obj, _ = Translation.objects.get_or_create(
        **{f"text_{TEMPLATE_LANGUAGE_REFERENCE}": key},
        defaults={f"text_{TEMPLATE_LANGUAGE_REFERENCE}": key},
    )

    value = getattr(obj, f"text_{lang_code}", None)

    if value:
        save_to_cache(key, lang_code, value)
        return value

    # 3. Перевод не найден — логируем и возвращаем оригинал
    logger.debug(f"⛔️ Перевод не найден | key='{key}' | lang='{lang_code}'")
    return key
