from django.views.generic import TemplateView
from apps.common.models import News


class HomeView(TemplateView):
    template_name = "common/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news'] = News.objects.exclude(is_active=False).order_by('-created_at')[:4]

        return context
