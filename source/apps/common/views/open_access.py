from django.views.generic import TemplateView


class OpenAccessView(TemplateView):
    template_name = 'common/open_access.html'
