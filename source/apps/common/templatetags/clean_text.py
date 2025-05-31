from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter
def clean_description(value, length=300):
    """
    Убирает HTML, спецсимволы и обрезает текст.
    """
    if not value:
        return ''

    text = strip_tags(value)
    text = text.replace('&nbsp;', ' ')

    text = ' '.join(text.split())

    if len(text) > length:
        return text[:length].rstrip() + '...'
    return text
