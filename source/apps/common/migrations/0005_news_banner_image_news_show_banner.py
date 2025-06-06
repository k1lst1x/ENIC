# Generated by Django 4.2 on 2025-05-31 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_tag_news_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='banner_image',
            field=models.FileField(blank=True, null=True, upload_to='news/pictures/', verbose_name='Картинка баннера'),
        ),
        migrations.AddField(
            model_name='news',
            name='show_banner',
            field=models.BooleanField(default=False, verbose_name='Показывать на главной в баннерах'),
        ),
    ]
