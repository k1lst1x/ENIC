from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Event(models.Model):
    title_ru = models.CharField(
        max_length=255,
        verbose_name="Название (RU)",
    )
    title_kz = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Название (KZ)",
    )
    title_en = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Название (EN)",
    )

    location_ru = models.CharField(
        max_length=255,
        verbose_name="Место проведения (RU)",
    )
    location_kz = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место проведения (KZ)",
    )
    location_en = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место проведения (EN)",
    )

    description_ru = CKEditor5Field(
        blank=True,
        verbose_name="Описание (RU)",
        config_name='extends'
    )
    description_kz = CKEditor5Field(
        blank=True,
        null=True,
        verbose_name="Описание (KZ)",
        config_name='extends'
    )
    description_en = CKEditor5Field(
        blank=True,
        null=True,
        verbose_name="Описание (EN)",
        config_name='extends'
    )

    datetime = models.DateTimeField(
        verbose_name="Дата и время проведения",
    )
    is_active = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ['-datetime']

    def __str__(self):
        return f"{self.title_ru} ({self.datetime.strftime('%d.%m.%Y')})"
