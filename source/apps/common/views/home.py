from django.views.generic import TemplateView
from apps.common.models import News, Event


class HomeView(TemplateView):
    template_name = "common/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        news = News.objects.exclude(is_active=False).order_by('-created_at')

        context['news'] = news[:4]
        context['slides'] = news.exclude(show_banner=False)
        context['week_days'] = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        context['events'] = Event.objects.filter(is_active=True).order_by('-datetime')[:10]

        return context
