from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..core.active_language_context import get_language
from ..core.translator import get_translate

register = template.Library()

# Названия месяцев для разных языков
MONTHS_BY_LANG = {
    'ru': {
        1: 'января',   2: 'февраля', 3: 'марта',   4: 'апреля',
        5: 'мая',      6: 'июня',    7: 'июля',    8: 'августа',
        9: 'сентября', 10: 'октября',11: 'ноября', 12: 'декабря',
    },
    'kz': {
        1: 'қаңтар',   2: 'ақпан',   3: 'наурыз',  4: 'сәуір',
        5: 'мамыр',    6: 'маусым',  7: 'шілде',   8: 'тамыз',
        9: 'қыркүйек', 10: 'қазан', 11: 'қараша', 12: 'желтоқсан',
    },
    'eng': {
        1: 'January',   2: 'February', 3: 'March',    4: 'April',
        5: 'May',       6: 'June',     7: 'July',     8: 'August',
        9: 'September',10: 'October', 11: 'November',12: 'December',
    },
}


@register.simple_tag
def url(view_name: str, *args, **kwargs) -> str:
    """
    Строит URL с префиксом активного языкового кода.
    Пример: {% url 'index' %} → /ru/index
    """
    lang = get_language()
    path = reverse(view_name, args=args, kwargs=kwargs)
    return f'/{lang}{path}'


@register.simple_tag
def tr(key: str) -> str:
    """
    Переводит строку по заданному ключу.
    Использует базу переводов из бд.
    """
    try:
        text = get_translate(key)
        return mark_safe(text)
    except Exception as exc:
        return f'Ошибка в теге tr: {exc}'


@register.filter(name='tr_date')
def tr_date(value) -> str: #только для этого проекта, не даёт гибкости и лимит языков возращает просто str
    """
    Форматирует дату согласно активному языку.
    Вывод: «день месяц год», где месяц — слово.
    """
    lang = get_language()
    months = MONTHS_BY_LANG.get(lang, MONTHS_BY_LANG['ru'])
    try:
        return f'{value.day} {months[value.month]} {value.year}'
    except Exception:
        return str(value)
