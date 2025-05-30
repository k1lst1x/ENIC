"""
Модель Translation — хранилище строк для мультиязычного перевода.

Каждая строка идентифицируется текстом на основном языке (TEMPLATE_LANGUAGE_REFERENCE).
Поле text_<lang_code> добавляется для каждого поддерживаемого языка.

🧠 Принцип:
- Строки в шаблонах, админке и API идентифицируются по значению на языке-шаблоне ('ru').
- Переводы хранятся в отдельных полях: text_ru, text_en, text_kk
- Перевод разрешается в рантайме через get_translate() и TrFieldBySuffix
"""

from django.db import models
from .core.conf import SUPPORTED_LANGUAGES, TEMPLATE_LANGUAGE_REFERENCE


class Translation(models.Model):
    """
    Модель для хранения переводов строк по всем поддерживаемым языкам.
    Текст на TEMPLATE_LANGUAGE_REFERENCE используется как уникальный ключ.
    """

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"

    def __str__(self) -> str:
        """
        Возвращает строку на языке шаблона или '[empty]', если поле пусто.
        """
        return getattr(self, f"text_{TEMPLATE_LANGUAGE_REFERENCE}", "[empty]")


# === Динамическое добавление полей text_<lang_code> для всех SUPPORTED_LANGUAGES ===

for lang in SUPPORTED_LANGUAGES:
    Translation.add_to_class(
        f"text_{lang['code']}",
        models.TextField(
            verbose_name=f"Текст на языке: {lang['name']}",
            unique=(lang["code"] == TEMPLATE_LANGUAGE_REFERENCE),  # основной язык — уникальный ключ
            null=(lang["code"] != TEMPLATE_LANGUAGE_REFERENCE),    # только он обязателен
            blank=(lang["code"] != TEMPLATE_LANGUAGE_REFERENCE),
            db_index=(lang["code"] == TEMPLATE_LANGUAGE_REFERENCE),  # нужен для быстрого поиска
        )
    )
