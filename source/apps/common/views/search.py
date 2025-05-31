from django.views.generic import TemplateView
from django.db.models import Q
from django.utils.translation import get_language

from apps.common.models import News, Event

class SearchView(TemplateView):
    template_name = "common/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        lang = get_language()

        if not query:
            context.update({
                'query': query,
                'news_results': [],
                'event_results': [],
                'total_results': 0,
            })
            return context

        title_field = f"title_{lang}"
        desc_field = f"small_description_{lang}"
        content_field = f"content_{lang}"
        event_desc_field = f"description_{lang}"

        news_q = Q(**{f"{title_field}__icontains": query}) | \
                 Q(**{f"{desc_field}__icontains": query}) | \
                 Q(**{f"{content_field}__icontains": query})

        event_q = Q(**{f"{title_field}__icontains": query}) | \
                  Q(**{f"{event_desc_field}__icontains": query})

        news_results = News.objects.filter(news_q, is_active=True)
        event_results = Event.objects.filter(event_q, is_active=True)

        context.update({
            'query': query,
            'news_results': news_results,
            'event_results': event_results,
            'total_results': news_results.count() + event_results.count()
        })
        return context
