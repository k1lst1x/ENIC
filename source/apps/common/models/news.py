from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.core.files.base import ContentFile
from django.utils.timezone import now
from io import BytesIO
from PIL import Image


class News(models.Model):
    title_ru = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name="Заголовок на русском"
    )
    title_kz = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Заголовок на казахском"
    )
    title_en = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Заголовок на английском"
    )

    image = models.FileField(
        upload_to='news/pictures/',
        verbose_name="Основная картинка новости",
    )

    small_description_ru = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name="Текст превью на русском"
    )
    small_description_kz = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Текст превью на казахском"
    )
    small_description_en = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Текст превью на английском"
    )
    tags = models.ManyToManyField(
        'common.Tag',
        related_name='news',
        verbose_name="Теги",
        blank=False
    )

    content_ru = CKEditor5Field(
        verbose_name='Контент на русском',
        config_name='extends'
    )
    content_kz = CKEditor5Field(
        null=True,
        blank=True,
        verbose_name='Контент на казахском',
        config_name='extends'
    )
    content_en = CKEditor5Field(
        null=True,
        blank=True,
        verbose_name='Контент на английском',
        config_name='extends'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Показать?"
    )

    created_at = models.DateField(
        default=now,
        verbose_name="Дата публикаций"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
        null=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.image = self.generate_image_version(self.image, 1.83, 'news_detail_image.jpg')  # 560:583
            super().save(*args, **kwargs)

    def crop_center(self, img, aspect_ratio):
        # Получаем текущие размеры изображения
        width, height = img.size

        # Рассчитываем новое соотношение сторон
        new_width = height * aspect_ratio
        new_height = width / aspect_ratio

        # Проверяем, что обрезать: по ширине или по высоте
        if new_width < width:
            # Обрезаем по ширине
            left = (width - new_width) / 2
            right = (width + new_width) / 2
            top = 0
            bottom = height
        else:
            # Обрезаем по высоте
            top = (height - new_height) / 2
            bottom = (height + new_height) / 2
            left = 0
            right = width

        # Обрезаем изображение по новым координатам
        img = img.crop((left, top, right, bottom))

        return img

    def generate_image_version(self, image_field, aspect_ratio, filename):
        img = Image.open(image_field)

        # Oбрезаем изображение до нужного соотношения сторон
        img = self.crop_center(img, aspect_ratio)

        # Convert 'P' (palette) or 'RGBA' mode images to 'RGB' for JPEG compatibility
        if img.mode in ('P', 'RGBA'):
            img = img.convert('RGB')

        # Сохраняем обработанное изображение в BytesIO объект
        img_io = BytesIO()
        img.save(img_io, format='JPEG')

        # Используем ContentFile для сохранения изображения в поле ImageField
        img_content = ContentFile(img_io.getvalue(), filename)
        return img_content

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title_ru[:50]
