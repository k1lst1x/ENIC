from django.views.generic import TemplateView


class SiteMapView(TemplateView):
    template_name = "common/sitemap.html"
