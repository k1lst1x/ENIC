"""
Контекст-процессор для шаблонов Django.

Зачем нужен:
Добавляет переменные, связанные с текущим языком, чтобы они были доступны в любом шаблоне — без дополнительной передачи через view.

Что делает:
- Получает текущий lang_code из локального потока (через get_language)
- Извлекает читаемое имя языка
- Формирует `current_path_without_lang` — путь без /<язык>/, чтобы переключатель языка не терял маршрут
- Возвращает список отображаемых языков в UI (code + name)

Где используется:
- В шаблонах: {{ current_lang_code }}, {{ current_lang_name }}
- В language switcher: <a href="/en{{ current_path_without_lang }}">EN</a>
"""

from .core.active_language_context import get_language
from .core.conf import (
    get_visible_languages,
    get_supported_language_codes,
    get_language_name,
)


def current_language(request) -> dict:
    """
    Возвращает словарь с языковым контекстом для шаблона.

    :param request: объект Django-запроса
    :return: словарь с переменными:
        - current_lang_code: активный lang_code, например 'kk'
        - current_lang_name: имя языка, например 'Қазақша'
        - current_path_without_lang: текущий путь без /<lang>/ + GET-параметры
        - show_languages_extended: список языков для переключателя
    """
    codes = get_supported_language_codes()
    lang_code = get_language()

    # Убираем префикс языка из пути, если он есть
    path_parts = request.path.strip("/").split("/")
    if path_parts and path_parts[0] in codes:
        trimmed_path = "/" + "/".join(path_parts[1:])
    else:
        trimmed_path = request.path or "/"

    # Добавляем GET-параметры обратно, если есть
    if request.META.get("QUERY_STRING"):
        trimmed_path += "?" + request.META["QUERY_STRING"]

    return {
        "current_lang_code": lang_code,
        "current_lang_name": get_language_name(lang_code),
        "current_path_without_lang": trimmed_path,
        "show_languages_extended": get_visible_languages(),
    }
