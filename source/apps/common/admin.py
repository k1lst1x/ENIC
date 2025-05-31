from django.contrib import admin
from .models import *


@admin.register(Tag)
class CustomAdminClass(admin.ModelAdmin):
    list_display = (
        'id',
        'slug',
        'name_ru',
        'name_kz',
        'name_en'
    )
    list_display_links = (
        'id',
        'slug',
        'name_ru',
        'name_kz',
        'name_en'
    )


@admin.register(News)
class CustomAdminClass(admin.ModelAdmin):
    list_display = (
        "id",
        'title_ru',
        'title_kz',
        'title_en',
        'is_active',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        "id",
        'title_ru',
        'title_kz',
        'title_en',
        'is_active',
        'created_at',
        'updated_at',
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title_ru',
        'datetime',
        'is_active',
    )
    list_filter = (
        'is_active',
        'datetime',
    )
    search_fields = (
        'title_ru', 'title_kz', 'title_en',
        'location_ru', 'location_kz', 'location_en',
    )
