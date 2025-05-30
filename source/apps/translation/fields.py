"""
Дескриптор TrFieldBySuffix — доступ к переведённым полям модели на основе активного языка (lang_code).

Принцип:
- В модели определены реальные поля, например: title_ru, title_en, title_kk.
- В коде/шаблонах используется виртуальное свойство: .title
- В момент вызова дескриптор возвращает значение из поля, соответствующего текущему языку, например:
  title_kk → если активен 'kk'
  title_en → если активен 'en'

Особенности:
- Если поле не определено в модели → AttributeError
- Если значение пустое (None, '', 'null') → вернёт пустую строку
- Безопасно возвращает HTML через mark_safe
"""

from typing import Any
from django.utils.safestring import mark_safe
from .core.active_language_context import get_language


class TrFieldBySuffix:
    """
    Виртуальное поле модели для получения перевода по текущему языку.
    
    :param field_base_name: базовое имя поля (например, 'title')
    """

    def __init__(self, field_base_name: str):
        self.field_base_name = field_base_name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        lang_code = get_language()
        translated_field = f"{self.field_base_name}_{lang_code}"

        if not hasattr(instance, translated_field):
            raise AttributeError(
                f"Модель '{instance.__class__.__name__}' не содержит поля '{translated_field}' "
                f"для языка '{lang_code}'. Убедитесь, что поле '{translated_field}' существует в модели."
            )

        value = getattr(instance, translated_field)
        return mark_safe(value) if self._is_valid(value) else ""

    @staticmethod
    def _is_valid(value: Any) -> bool:
        """
        Проверяет, является ли значение допустимым (не None, не пустым, не 'null')
        """
        if value is None:
            return False
        if isinstance(value, str):
            v = value.strip().lower()
            return bool(v and v not in {"none", "null"})
        return True

    def __str__(self):
        return f"TrFieldBySuffix({self.field_base_name})"
