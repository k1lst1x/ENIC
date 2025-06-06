# Generated by Django 4.2 on 2025-05-31 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='small_description_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Текст превью на английском'),
        ),
        migrations.AlterField(
            model_name='news',
            name='small_description_kz',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Текст превью на казахском'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title_en',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Заголовок на английском'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title_kz',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Заголовок на казахском'),
        ),
    ]
