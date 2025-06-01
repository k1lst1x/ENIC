from django.views.generic import TemplateView


class FaqView(TemplateView):
    template_name = 'common/faq.html'
