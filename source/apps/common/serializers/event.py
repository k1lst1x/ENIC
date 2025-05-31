from rest_framework import serializers
from django.utils.translation import get_language


class EventDaySerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_title(self, obj):
        lang = self.context.get('lang', get_language())
        return getattr(obj, f"title_{lang}", None) or obj.title_ru

    def get_location(self, obj):
        lang = self.context.get('lang', get_language())
        return getattr(obj, f"location_{lang}", None) or obj.location_ru

    def get_time(self, obj):
        return obj.datetime.strftime('%d.%m.%Y, %H:%M')
