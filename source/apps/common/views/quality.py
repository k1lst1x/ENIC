from django.views.generic import TemplateView


class QualityView(TemplateView):
    template_name = 'common/quality.html'
