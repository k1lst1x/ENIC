"""
CustomLocaleMiddleware — middleware для поддержки мультиязычности через URL.

Функции:
1. Извлекает язык из URL (например, /ru/)
2. Если язык отсутствует — выполняет редирект на URL с языковым префиксом
3. Устанавливает язык в локальный поток (через set_language)
4. (опционально) активирует Django-переводы через activate()
"""

import logging
from django.http import HttpResponseRedirect
from django.utils.translation import activate as django_activate, get_supported_language_variant

from .core.active_language_context import set_language
from .core.conf import (
    get_supported_language_codes,
    DEFAULT_LANGUAGE_STARTUP,
    ENABLE_DJANGO_TRANSLATION_ACTIVATE,
    LANGUAGE_EXCLUDED_URL_PREFIXES,
)

logger = logging.getLogger("translation.middleware")


class CustomLocaleMiddleware:
    """
    Middleware, который извлекает языковой код из URL и применяет:
    - Кастомный перевод на основе локального контекста потока
    - При необходимости вызывает activate() от Django для совместимости
    - Редиректит на URL с языком, если язык отсутствует в URL
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_codes = set(get_supported_language_codes())
        self.excluded_prefixes = tuple(LANGUAGE_EXCLUDED_URL_PREFIXES)

    def __call__(self, request):
        path_parts = request.path.split("/")
        lang = None

        # === Язык указан в URL (например, /ru/...)
        if len(path_parts) > 1 and path_parts[1] in self.supported_codes:
            lang = path_parts[1]
            request.path_info = "/" + "/".join(path_parts[2:])
            request.session["django_language"] = lang

        else:
            # === Язык не указан — пробуем из сессии или по умолчанию
            lang = request.session.get("django_language", DEFAULT_LANGUAGE_STARTUP)

            # === Редирект на /<lang>/... если путь не исключён
            if not request.path.startswith(self.excluded_prefixes):
                redirect_path = f"/{lang}{request.path}"
                if request.GET:
                    redirect_path += f"?{request.GET.urlencode()}"
                return HttpResponseRedirect(redirect_path)

        # === Проверка на случай некорректного кода языка
        if lang not in self.supported_codes:
            lang = DEFAULT_LANGUAGE_STARTUP

        # === Установка кастомного языка (контекст потока)
        set_language(lang)
        request.LANGUAGE_CODE = lang

        # === (Опционально) активация Django gettext
        if ENABLE_DJANGO_TRANSLATION_ACTIVATE:
            try:
                django_activate(get_supported_language_variant(lang))
            except Exception:
                logger.info(f"Django не поддерживает язык '{lang}', activate() пропущен.")

        return self.get_response(request)
