from rest_framework.views import APIView
from rest_framework.response import Response
from apps.common.models import Event
from django.views.generic import DetailView, ListView
from django.utils.timezone import localtime
from django.utils.translation import get_language
import json

from apps.common.serializers import EventDaySerializer


class EventsByMonthAPIView(APIView):
    def get(self, request):
        try:
            year = int(request.GET.get("year"))
            month = int(request.GET.get("month"))
        except (TypeError, ValueError):
            return Response({"error": "Invalid year or month"}, status=400)

        lang = request.GET.get("lang") or request.LANGUAGE_CODE
        events = Event.objects.filter(
            datetime__year=year,
            datetime__month=month,
            is_active=True,
        )

        grouped = {}
        for event in events:
            day = str(event.datetime.day)
            grouped.setdefault(day, []).append(event)

        result = {}
        for day, event_list in grouped.items():
            serializer = EventDaySerializer(event_list, many=True, context={"lang": lang})
            result[day] = serializer.data

        return Response(result)


class EventDetailView(DetailView):
    template_name = 'events/event_detail.html'
    model = Event
    context_object_name = 'event'

    def get_queryset(self):
        # Показывать только активные события
        return Event.objects.filter(is_active=True)


class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event
    context_object_name = 'events'
    ordering = ['-datetime']

    def get_queryset(self):
        return Event.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = self.get_queryset()

        # Язык пользователя
        lang = get_language()

        def get_field(obj, field_base):
            return getattr(obj, f'{field_base}_{lang}', '') or getattr(obj, f'{field_base}_ru', '')

        context['events_json'] = json.dumps([
            {
                "id": event.id,
                "title": get_field(event, 'title'),
                "location": get_field(event, 'location'),
                "description": get_field(event, 'description'),
                "datetime": localtime(event.datetime).strftime('%d.%m.%Y'),
                "day": localtime(event.datetime).day,
                "month": localtime(event.datetime).month,
                "month_name": localtime(event.datetime).strftime('%B'),
                "year": localtime(event.datetime).year,
                "time": localtime(event.datetime).strftime('%H:%M'),
                "views": 0,  # можно заменить на event.views если есть поле
            }
            for event in events
        ])
        return context
