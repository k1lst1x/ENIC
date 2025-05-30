import csv
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings

from .models import Translation
from .core.conf import SUPPORTED_LANGUAGES, TEMPLATE_LANGUAGE_REFERENCE


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Translation с динамическими языковыми полями
    и экспортом переводов в CSV.
    """

    base_list_display = ["id", "updated_at"]
    base_search_fields = ["id"]
    language_fields = [f"text_{lang['code']}" for lang in SUPPORTED_LANGUAGES]

    list_display = base_list_display + language_fields
    search_fields = base_search_fields + language_fields
    list_filter = ["updated_at"]
    ordering = ["-updated_at"]
    actions = ["export_as_csv"]

    def get_list_display(self, request):
        return self.base_list_display + self.language_fields[:4]

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if not settings.DEBUG:
            main_field = f"text_{TEMPLATE_LANGUAGE_REFERENCE}"
            return readonly + (main_field,)
        return readonly

    @admin.action(description="Скачать выбранные переводы в CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=translations.csv"

        writer = csv.writer(response)
        headers = ["ID"] + self.language_fields
        writer.writerow(headers)

        for obj in queryset:
            row = [obj.id] + [getattr(obj, field, "") for field in self.language_fields]
            writer.writerow(row)

        return response
