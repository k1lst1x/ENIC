from django.views.generic.base import TemplateView


class ProjectsView(TemplateView):
    template_name = "common/projects.html"